# ======================================================================= #
# Copyright (C) 2023 Hoverset Group.                                      #
# ======================================================================= #

import tkinter as tk
from collections import defaultdict

from hoverset.platform import platform_is, WINDOWS, LINUX
from hoverset.ui.widgets import EventMask
from hoverset.ui.icons import get_icon_image


def resize_cursor() -> tuple:
    r"""
    Returns a tuple of the cursors to be used based on platform
    :return: tuple ("nw_se", "ne_sw") cursors roughly equal to \ and / respectively
    """
    if platform_is(WINDOWS):
        # Windows provides corner resize cursors so use those
        return "size_nw_se", "size_ne_sw"
    if platform_is(LINUX):
        return "bottom_right_corner", "bottom_left_corner"
    # Use circles for other platforms
    return ("circle",) * 2


class Dot(tk.Frame):
    _corner_cursors = resize_cursor()
    _cursor_map = dict(
        n="sb_v_double_arrow",
        s="sb_v_double_arrow",
        e="sb_h_double_arrow",
        w="sb_h_double_arrow",
        c="fleur",
        nw=_corner_cursors[0],
        ne=_corner_cursors[1],
        sw=_corner_cursors[1],
        se=_corner_cursors[0],
        all="fleur"
    )

    def __init__(self, handle, direction):
        super().__init__(handle.master)
        self.direction = direction
        color = handle.master.style.colors["accent"]
        border = handle.master.style.colors["primarydarkaccent"]
        self.config(
            width=6, height=6, bg=color, cursor=self._cursor_map[direction],
            highlightthickness=1, highlightbackground=border
        )
        self.handle = handle
        self.bind("<ButtonPress>", self.on_press)
        self.bind("<ButtonRelease>", self.on_release)
        self.bind("<Motion>", self.on_move)
        self.fix = (0, 0)

    def on_move(self, event):
        if not event.state & EventMask.MOUSE_BUTTON_1:
            return
        x, y = self.fix
        self.fix = (event.x_root, event.y_root)
        self.handle.on_dot_move(self.direction, (event.x_root - x, event.y_root - y))

    def on_press(self, event):
        self.fix = (event.x_root, event.y_root)
        self.handle.set_direction(self.direction)

    def on_release(self, _):
        self.handle.set_direction(None)

    def set_direction(self, direction):
        self.direction = direction
        self.config(cursor=self._cursor_map[direction])


class Edge(tk.Frame):

    def __init__(self, handle):
        super().__init__(handle.master)
        color = handle.master.style.colors["accent"]
        self.config(bg=color, height=2, width=2)


class Handle:

    _pool = defaultdict(list)

    def __init__(self, widget, master=None):
        self.widget = widget
        self.master = widget if master is None else master
        self.active_direction = None
        self.dots = []
        self.edges = []
        self.label = None
        self._hover = False
        self._showing = False
        self.allow_move = False

    def set_direction(self, direction):
        if direction is None:
            self.widget.handle_inactive(self.active_direction)
            self.active_direction = None
            return
        self.active_direction = direction
        self.widget.handle_active(direction)

    def on_dot_move(self, direction, delta):
        self.widget.handle_resize(direction, delta)

    def widget_config_changed(self):
        pass

    def lift(self):
        for dot in self.dots:
            dot.lift()
        for edge in self.edges:
            edge.lift()

    def redraw(self):
        raise NotImplementedError

    def active(self):
        return self._showing or self._hover

    def show(self):
        if self._showing:
            return
        self._showing = True
        self.redraw()

    def hide(self):
        if not self._showing:
            return
        for dot in self.dots:
            dot.place_forget()
        self._showing = False
        if not self._hover:
            self.release()

    def hover(self):
        if self._hover:
            return
        self._hover = True
        self.redraw()

    def unhover(self):
        if not self._hover:
            return
        for edge in self.edges:
            edge.place_forget()
        if self.label:
            self.label.place_forget()
        self._hover = False
        self.redraw()
        if not self._showing:
            self.release()

    def release(self):
        Handle._pool[(self.__class__, self.master)].append(self)

    @classmethod
    def acquire(cls, widget, master=None, move=False):
        master = widget if master is None else master
        if not cls._pool[(cls, master)]:
            obj = cls(widget, master)
        else:
            obj = cls._pool[(cls, master)].pop()
            obj.widget = widget
        obj.lift()
        obj.allow_move = move
        return obj


class BoxHandle(Handle):
    move_icon = None

    def __init__(self, widget, master=None):
        super().__init__(widget, master)
        self.directions = ["n", "s", "e", "w", "nw", "ne", "sw", "se", "all"]
        self.dots = [Dot(self, direction) for direction in self.directions]
        BoxHandle.move_icon = BoxHandle.move_icon or get_icon_image("move", 12, 12, color="#ffffff")
        label = tk.Label(
            self.dots[-1],
            image=BoxHandle.move_icon,
            bg=master.style.colors["accent"]
        )
        label.pack(fill="both", expand=True)
        self.dots[-1].config(width=12, height=12)
        self.dots[-1].pack_propagate(False)
        label.bind("<ButtonPress>", self.dots[-1].on_press)
        label.bind("<ButtonRelease>", self.dots[-1].on_release)
        label.bind("<Motion>", self.dots[-1].on_move)

    def redraw(self):
        if self._showing:
            n, s, e, w, nw, ne, sw, se, c = self.dots
            radius = 3
            # border-mode has to be outside so the highlight covers the entire widget
            extra = dict(in_=self.widget, bordermode="outside")
            nw.place(**extra, x=-radius, y=-radius)
            ne.place(**extra, relx=1, x=-radius, y=-radius)
            sw.place(**extra, x=-radius, rely=1, y=-radius)
            se.place(**extra, relx=1, x=-radius, rely=1, y=-radius)
            n.place(**extra, relx=0.5, x=-radius, y=-radius)
            s.place(**extra, relx=0.5, x=-radius, rely=1, y=-radius)
            e.place(**extra, relx=1, x=-radius, rely=0.5, y=-radius)
            w.place(**extra, x=-radius, rely= 0.5, y=-radius)

            if not self.allow_move:
                c.place(**extra, relx=1, x=-24, rely=1, y=-6)

        if self._hover:
            if not self.edges:
                self.edges = [Edge(self) for _ in range(4)]
            if not self.label:
                self.label = tk.Label(self.master, **self.master.style.text_small)
                self.label.config(bg=self.master.style.colors["accent"], fg="#ffffff")
            self.label.config(text=f"{self.widget.id}")
            self.label.place(
                in_=self.master, bordermode="outside",
                x=self.widget.winfo_x(), y=self.widget.winfo_y(), anchor="sw"
            )
            extra = dict(in_=self.widget, bordermode="outside")
            n, s, e, w = self.edges
            n.place(**extra, x=0, y=0, relwidth=1)
            e.place(**extra, relx=1, x=-e['width'], y=0, relheight=1)
            s.place(**extra, rely=1, y=-e['width'], x=0, relwidth=1)
            w.place(**extra, x=0, y=0, relheight=1)


class LinearHandle(Handle):

    def __init__(self, widget, master=None):
        super().__init__(widget, master)
        self.start = Dot(self, "w")
        self.end = Dot(self, "e")
        self.center = Dot(self, "all")
        self.dots = [self.start, self.end, self.center]
        self.orient = 'horizontal'

    def _get_orientation(self):
        try:
            return self.widget.cget("orient")
        except tk.TclError:
            return "horizontal"

    def widget_config_changed(self):
        if str(self._get_orientation()) != self.orient:
            self.orient = str(self._get_orientation())
            for dot in self.dots:
                dot.place_forget()
            self.redraw()

    def redraw(self):
        if self._showing:
            radius = 2
            extra = dict(in_=self.widget, bordermode="outside")

            if self.orient == "horizontal":
                self.start.set_direction("w")
                self.end.set_direction("e")
                self.center.set_direction("all")
                self.start.place(**extra, x=-radius, y=-radius)
                self.end.place(**extra, relx=1, x=-radius, y=-radius)
                self.center.place(**extra, relx=0.5, x=-radius, y=-radius)
            else:
                self.start.set_direction("n")
                self.end.set_direction("s")
                self.center.set_direction("all")
                self.start.place(**extra, x=-radius, y=-radius)
                self.end.place(**extra, x=-radius, rely=1, y=-radius)
                self.center.place(**extra, rely=0.5,x=-radius, y=-radius)
