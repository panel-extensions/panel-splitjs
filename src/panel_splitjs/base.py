from pathlib import Path

import param
from bokeh.embed.bundle import extension_dirs
from panel.custom import Children, JSComponent
from panel.layout.base import ListLike

BASE_PATH = Path(__file__).parent
DIST_PATH = BASE_PATH / 'dist'

extension_dirs['panel-splitjs'] = DIST_PATH


class Size(param.Parameter):

    __slots__ = ['length']

    def __init__(self, default=None, length=None, **params):
        super().__init__(default=default, **params)
        self.length = length

    def _validate(self, val):
        super()._validate(val)
        if val is None:
            return
        if self.length is not None and isinstance(val, tuple) and len(val) != self.length:
            raise ValueError(f"Size parameter {self.name!r} must have length {self.length}")
        if not (isinstance(val, (int, float)) or (isinstance(val, tuple) and all(isinstance(v, (int, float)) for v in val))):
            raise ValueError(f"Size parameter {self.name!r} only takes int or float values")


class SplitBase(JSComponent, ListLike):

    max_size = Size(default=None, doc="""
        The maximum sizes of the panels (in pixels) either as a single value or a tuple.""")

    min_size = Size(default=None, doc="""
        The minimum sizes of the panels (in pixels) either as a single value or a tuple.""")

    objects = Children(doc="""
        The list of child objects that make up the layout.""")

    orientation = param.Selector(default="horizontal", objects=["horizontal", "vertical"], doc="""
        The orientation of the split panel. Default is horizontal.""")

    sizes = param.NumericTuple(default=None, length=0, doc="""
        The sizes of the panels (as percentages) on initialization. The value is automatically
        synced to the sizes of the panels in the frontend.""")

    step_size = param.Integer(default=1, doc="""
        The step size (in pixels) at which the size of the panels can be changed.""")

    snap_size = param.Integer(default=30, doc="""
        Snap to minimum size at this offset in pixels.""")

    _bundle = DIST_PATH  / "panel-splitjs.bundle.js"
    _stylesheets = [DIST_PATH / "css" / "splitjs.css"]
    _render_policy = "manual"

    __abstract = True

    def _process_property_change(self, props):
        props = super()._process_property_change(props)
        if 'sizes' in props:
            props['sizes'] = tuple(props['sizes'])
        return props


class Split(SplitBase):
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

    collapsed = param.Integer(default=None, doc="""
        Whether the first or second panel is collapsed. 0 for first panel, 1 for second panel, None for not collapsed.""")

    expanded_sizes = param.NumericTuple(default=(50, 50), length=2, doc="""
        The sizes of the two panels when expanded (as percentages).
        Default is (50, 50) .
        When invert=True, these percentages are automatically swapped.""")

    max_size = Size(default=None, length=2, doc="""
        The maximum sizes of the panels (in pixels) either as a single value or a tuple of two values.""")

    min_size = Size(default=0, length=2, doc="""
        The minimum sizes of the panels (in pixels) either as a single value or a tuple of two values.""")

    objects = Children(doc="""
        The component to place in the left panel.
        When invert=True, this will appear on the right side.""")

    show_buttons = param.Boolean(default=True, doc="""
        Whether to show the toggle buttons on the divider.
        When False, the buttons are hidden and panels can only be resized by dragging.""")

    sizes = param.NumericTuple(default=(50, 50), length=2, doc="""
        The initial sizes of the two panels (as percentages).
        Default is (50, 50) which means the left panel takes up 50% of the space
        and the right panel is not visible.""")

    _esm = Path(__file__).parent / "models" / "split.js"

    def __init__(self, *objects, **params):
        if objects:
            params["objects"] = list(objects)
        if "objects" in params:
            objects = params["objects"]
            if len(objects) > 2:
                raise ValueError("Split component must have at most two children.")
        super().__init__(**params)


class HSplit(Split):
    """
    HSplit is a component for creating a responsive horizontal split panel layout.
    """

    orientation = param.Selector(default="horizontal", objects=["horizontal"], readonly=True)


class VSplit(Split):
    """
    VSplit is a component for creating a responsive vertical split panel layout.
    """

    orientation = param.Selector(default="vertical", objects=["vertical"], readonly=True)


class MultiSplit(SplitBase):
    """
    MultiSplit is a component for creating a responsive multi-split panel layout.
    """

    min_size = Size(default=100, length=None, doc="""
        The minimum sizes of the panels (in pixels) either as a single value or a tuple.""")

    _esm = Path(__file__).parent / "models" / "multi_split.js"

    def __init__(self, *objects, **params):
        if objects:
            params["objects"] = list(objects)
        if "objects" in params:
            objects = params["objects"]
            self.param.sizes.length = len(objects)
        super().__init__(**params)

    @param.depends("objects", watch=True)
    def _update_sizes(self):
        self.param.sizes.length = len(self.objects)


__all__ = ["HSplit", "MultiSplit", "Split", "VSplit"]
