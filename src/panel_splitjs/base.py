from pathlib import Path
from typing import Any

import param

from bokeh.embed.bundle import extension_dirs
from panel.custom import Children, JSComponent
from panel.layout.base import ListLike


BASE_PATH = Path(__file__).parent
DIST_PATH = BASE_PATH / 'dist'

extension_dirs['panel-splitjs'] = DIST_PATH


class SplitChildren(Children):
    """A Children parameter that only allows at most two items."""

    def _validate(self, val):
        super()._validate(val)
        if len(val) > 2:
            raise ValueError("Split component must have at most two children.")
        elif len(val) == 1:
            val.append(val[0])
        elif len(val) == 0:
            val = [None, None]
        return val


class Split(JSComponent, ListLike):
    """
    Split is a component for creating a responsive split panel layout.

    This component uses split.js to create a draggable split layout with two panels.

    Key features include:
    - Collapsible panels with toggle button
    - Minimum size constraints for each panel
    - Invertible layout to support different UI configurations
    - Responsive sizing with automatic adjustments
    - Animation for better user experience

    The component is ideal for creating application layouts with a main content area
    and a secondary panel that can be toggled (like a chat interface with output display).
    """

    collapsed = param.Boolean(default=False, doc="""
        Whether the secondary panel is collapsed.
        When True, only one panel is visible (determined by invert).
        When False, both panels are visible according to expanded_sizes.""")

    expanded_sizes = param.NumericTuple(default=(50, 50), length=2, doc="""
        The sizes of the two panels when expanded (as percentages).
        Default is (50, 50) which means the left panel takes up 35% of the space
        and the right panel takes up 65% when expanded.
        When invert=True, these percentages are automatically swapped.""")

    invert = param.Boolean(default=False, constant=True, doc="""
        Whether to invert the layout, changing the toggle button side and panel styles.""")

    min_sizes = param.NumericTuple(default=(0, 0), length=2, doc="""
        The minimum sizes of the two panels (in pixels).
        Default is (0, 0) which allows both panels to fully collapse.
        Set to (300, 0) or similar values if you want to enforce minimum widths during dragging.
        When invert=True, these values are automatically swapped.""")

    objects = SplitChildren(doc="""
        The component to place in the left panel.
        When invert=True, this will appear on the right side.""")

    orientation = param.Selector(default="horizontal", objects=["horizontal", "vertical"], doc="""
        The orientation of the split panel. Default is horizontal.""")

    show_buttons = param.Boolean(default=False, doc="""
        Whether to show the toggle buttons on the divider.
        When False, the buttons are hidden and panels can only be resized by dragging.""")

    sizes = param.NumericTuple(default=(100, 0), length=2, doc="""
        The initial sizes of the two panels (as percentages).
        Default is (100, 0) which means the left panel takes up all the space
        and the right panel is not visible.""")

    _bundle = DIST_PATH  / "panel-splitjs.bundle.js"
    _esm = Path(__file__).parent / "models" / "splitjs.js"

    _stylesheets = [DIST_PATH / "css" / "splitjs.css"]

    def __init__(self, *objects, **params):
        if objects:
            params["objects"] = list(objects)
        super().__init__(**params)
        if self.invert:
            # Swap min_sizes when inverted
            left_min, right_min = self.min_sizes
            self.min_sizes = (right_min, left_min)

            # Swap expanded_sizes when inverted
            left_exp, right_exp = self.expanded_sizes
            self.expanded_sizes = (right_exp, left_exp)

    @param.depends("collapsed", watch=True)
    def _send_collapsed_update(self):
        """Send message to JS when collapsed state changes in Python"""
        self._send_msg({"type": "update_collapsed", "collapsed": self.collapsed})

    def _handle_msg(self, msg):
        """Handle messages from JS"""
        if 'collapsed' in msg:
            collapsed = msg['collapsed']
            with param.discard_events(self):
                # Important to discard so when user drags the panel, it doesn't
                # expand to the expanded sizes
                self.collapsed = collapsed


class HSplit(Split):

    orientation = param.Selector(default="horizontal", objects=["horizontal"], readonly=True)


class VSplit(Split):

    orientation = param.Selector(default="vertical", objects=["vertical"], readonly=True)


__all__ = ["HSplit", "Split", "VSplit"]
