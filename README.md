# panel-splitjs

[![CI](https://img.shields.io/github/actions/workflow/status/panel-extensions/panel-splitjs/ci.yml?style=flat-square&branch=main)](https://github.com/panel-extensions/panel-splitjs/actions/workflows/ci.yml)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/panel-splitjs?logoColor=white&logo=conda-forge&style=flat-square)](https://prefix.dev/channels/conda-forge/packages/panel-splitjs)
[![pypi-version](https://img.shields.io/pypi/v/panel-splitjs.svg?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/panel-splitjs)
[![python-version](https://img.shields.io/pypi/pyversions/panel-splitjs?logoColor=white&logo=python&style=flat-square)](https://pypi.org/project/panel-splitjs)

A responsive, draggable split panel component for [Panel](https://panel.holoviz.org) applications, powered by [split.js](https://split.js.org/).

## Features

- **Draggable dividers** - Resize panels by dragging the divider between them
- **Collapsible panels** - Collapse individual panels with toggle buttons
- **Flexible orientation** - Support for both horizontal and vertical splits
- **Size constraints** - Enforce minimum and maximum panel sizes
- **Snap behavior** - Smart snapping to minimum sizes for better UX
- **Customizable sizes** - Control initial and expanded panel sizes
- **Multi-panel support** - Create layouts with 2+ panels using `MultiSplit`

## Installation

Install via pip:

```bash
pip install panel-splitjs
```

Or via conda:

```bash
conda install -c conda-forge panel-splitjs
```

## Quick Start

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Create a simple split layout
split = Split(
    pn.pane.Markdown("## Left Panel\nContent here", width=150),
    pn.pane.Markdown("## Right Panel\nMore content", width=150),
    sizes=(50, 50),  # Equal sizing initially
    min_size=150,     # Minimum 150px for each panel
    sizing_mode="stretch_both",
)

split.servable()
```

![Quick Start Example](docs/assets/images/quick-start.gif)

## Usage Examples

### Basic Horizontal Split

```python
import panel as pn
from panel_splitjs import HSplit

pn.extension(sizing_mode="stretch_width")

left_panel = pn.Column(
    "# Main Content",
    pn.widgets.TextInput(name="Input"),
    pn.pane.Markdown("This is the main content area."),
    margin=25, # To separate toggle button and column
)

right_panel = pn.Column(
    "# Sidebar",
    pn.widgets.Select(name="Options", options=["A", "B", "C"]),
    margin=25, # To separate toggle button and column
)

split = HSplit(
    left_panel,
    right_panel,
    sizes=(70, 30),  # 70% left, 30% right
    min_size=300,    # Minimum 300px for each panel
    sizing_mode="stretch_width",
    height=250,
)

split.servable()
```

![Basic Horizontal Split Example](docs/assets/images/basic-horizontal-split.png)

### Vertical Split

```python
import panel as pn
from panel_splitjs import VSplit

pn.extension()

top_panel = pn.pane.Markdown("## Top Section\nHeader content")
bottom_panel = pn.pane.Markdown("## Bottom Section\nFooter content")

split = VSplit(
    top_panel,
    bottom_panel,
    sizes=(70, 30),
    min_size=200,
    height=600,
    sizing_mode="stretch_width"
)

split.servable()
```

![Basic Vertical Split Example](docs/assets/images/basic-vertical-split.png)

### Show Buttons

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Create a simple split layout
split = Split(
    pn.pane.Markdown("## Left Panel\nContent here", width=150),
    pn.pane.Markdown("## Right Panel\nMore content", width=150),
    sizes=(50, 50),  # Equal sizing initially
    min_size=150,     # Minimum 150px for each panel
    show_buttons=True,
    sizing_mode="stretch_both",
)

split.servable()
```

![Show Buttons Example](docs/assets/images/show-buttons.png)

### Collapsible Sidebar

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Start with right panel collapsed
button = pn.widgets.Button(name="Toggle Sidebar")

split = Split(
    pn.Column(pn.pane.Markdown("## Main Content"), button),
    pn.pane.Markdown("## Collapsible Sidebar", margin=(10,10,10,25)),
    collapsed=1,  # 0 for first panel, 1 for second panel, None for not collapsed
    expanded_sizes=(80, 20),  # When expanded, 80% main, 20% sidebar
    sizing_mode="stretch_both",
)

# Toggle collapse programmatically

def toggle(event):
    split.collapsed = None if split.collapsed == 1 else 1
button.on_click(toggle)

split.servable()
```

![Collapsible Sidebar Example](docs/assets/images/collapsable-sidebar.gif)

### Multi-Panel Split

```python
import panel as pn
from panel_splitjs import MultiSplit

pn.extension()

# Create a layout with three panels
multi = MultiSplit(
    pn.pane.Markdown("## Panel 1"),
    pn.pane.Markdown("## Panel 2"),
    pn.pane.Markdown("## Panel 3"),
    sizes=(30, 40, 30),  # Three panels with custom sizing
    min_size=100,        # Minimum 100px for each panel
    orientation="horizontal",
    sizing_mode="stretch_both",
)

multi.servable()
```

![MultiSplit Example](docs/assets/images/multisplit.png)

## API Reference

### Split

The main split panel component for creating two-panel layouts with collapsible functionality.

**Parameters:**

- `objects` (list): Two Panel components to display in the split panels
- `collapsed` (int | None, default=None): Which panel is collapsed - `0` for first panel, `1` for second panel, `None` for not collapsed
- `expanded_sizes` (tuple, default=(50, 50)): Percentage sizes when both panels are expanded
- `max_size` (int | tuple, default=None): Maximum sizes in pixels - single value applies to both panels, tuple for individual sizes
- `min_size` (int | tuple, default=0): Minimum sizes in pixels - single value applies to both panels, tuple for individual sizes
- `orientation` (str, default="horizontal"): Either `"horizontal"` or `"vertical"`
- `show_buttons` (bool, default=False): Show collapse/expand toggle buttons on the divider
- `sizes` (tuple, default=(50, 50)): Initial percentage sizes of the panels
- `snap_size` (int, default=30): Snap to minimum size at this offset in pixels
- `step_size` (int, default=1): Step size in pixels at which panel sizes can be changed

### HSplit

Horizontal split panel (convenience class).

Same parameters as `Split` but `orientation` is locked to `"horizontal"`.

### VSplit

Vertical split panel (convenience class).

Same parameters as `Split` but `orientation` is locked to `"vertical"`.

### MultiSplit

Multi-panel split component for creating layouts with three or more panels.

**Parameters:**

- `objects` (list): List of Panel components to display (3 or more)
- `max_size` (int | tuple, default=None): Maximum sizes in pixels - single value applies to all panels, tuple for individual sizes
- `min_size` (int | tuple, default=100): Minimum sizes in pixels - single value applies to all panels, tuple for individual sizes
- `orientation` (str, default="horizontal"): Either `"horizontal"` or `"vertical"`
- `sizes` (tuple, default=None): Initial percentage sizes of the panels (length must match number of objects)
- `snap_size` (int, default=30): Snap to minimum size at this offset in pixels
- `step_size` (int, default=1): Step size in pixels at which panel sizes can be changed

## Common Use Cases

### Chat Interface with Output

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

with pn.config.set(sizing_mode="stretch_width"):
    chat = pn.chat.ChatInterface(margin=(5,25,5,5))
    output = pn.Column("# Output Area")

split = Split(
    chat,
    output,
    collapsed=None,  # Both panels visible
    expanded_sizes=(50, 50),
    min_size=(600, 300),  # Minimum 600px for the first panel, 300px for the second panel
    sizing_mode="stretch_both",
)

split.servable()
```

![Chat Example](docs/assets/images/chat-example.png)

### Dashboard with Collapsible Controls

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

with pn.config.set(sizing_mode="stretch_width"):
    controls = pn.Column(
        pn.widgets.Select(name="Dataset", options=["A", "B", "C"]),
        pn.widgets.IntSlider(name="Threshold", start=0, end=100),
        pn.widgets.Button(name="Update"),
        margin=(5,20,5,5),
    )

    visualization = pn.pane.Markdown("## Main Visualization Area")

split = Split(
    controls,
    visualization,
    sizes=(20, 80),
    min_size=(300, 0),
    show_buttons=True,
    sizing_mode="stretch_both",
)

split.servable()
```

![Dashboard with Collapsible Controls](docs/assets/images/dashboard-with-collapsable-controls.png)

### Responsive Layout with Size Constraints

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

split = Split(
    pn.pane.Markdown("## Panel 1\nResponsive content", sizing_mode="stretch_width", margin=(5,25,5,5)),
    pn.pane.Markdown("## Panel 2\nMore responsive content", sizing_mode="stretch_width", margin=(5,5,5,25)),
    sizes=(50, 50),
    min_size=200,        # Minimum 200px per panel
    max_size=800,        # Maximum 800px per panel
    snap_size=50,        # Snap to min size when within 50px
    show_buttons=True,
    sizing_mode="stretch_both",
)

split.servable()
```

![Responsive Layout with Size Constraints](docs/assets/images/responsive-layout-with-size-constraints.png)

### Complex Multi-Panel Layout

```python
import panel as pn
from panel_splitjs import MultiSplit

pn.extension()

# Create a four-panel layout
with pn.config.set(sizing_mode="stretch_width"):
    sidebar = pn.Column("## Sidebar", pn.widgets.Select(options=["A", "B", "C"]))
    main = pn.pane.Markdown("## Main Content Area")
    detail = pn.pane.Markdown("## Detail Panel")
    console = pn.pane.Markdown("## Console Output")

multi = MultiSplit(
    sidebar,
    main,
    detail,
    console,
    sizes=(15, 40, 25, 20),  # Custom sizing for each panel
    min_size=(150, 300, 200, 150),  # Individual minimums
    orientation="horizontal",
    sizing_mode="stretch_both",
)

multi.servable()
```

![Complex Multi-Panel Layout](docs/assets/images/complex-multi-panel-layout.png)

### Nested Splits

```python
import panel as pn
from panel_splitjs import HSplit, VSplit

pn.extension()

# Create a nested layout: horizontal split with vertical split on right
left = pn.pane.Markdown("## Left Panel")

# Right side has a vertical split
with pn.config.set(sizing_mode="stretch_both"):
    top_right = pn.pane.Markdown("## Top Right")
    bottom_right = pn.pane.Markdown("## Bottom Right")
    right = VSplit(top_right, bottom_right, sizes=(60, 40))

    # Main horizontal split
    layout = HSplit(
        left,
        right,
        sizes=(30, 70),
        min_size=200,
        sizing_mode="stretch_both",
    )

layout.servable()
```

![Nested Splits](docs/assets/images/nested-splits.png)

## Development

This project is managed by [pixi](https://pixi.sh).

### Setup

```bash
git clone https://github.com/panel-extensions/panel-splitjs
cd panel-splitjs

pixi run pre-commit-install
pixi run postinstall
pixi run test
```

### Building

```bash
pixi run build
```

### Testing

```bash
pixi run test
```

### Pre-commit

Before committing the first time please install `pre-commit`:

```bash
pip install pre-commit
pre-commit install
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.
