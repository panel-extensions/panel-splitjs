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
    pn.pane.Markdown("## Left Panel\nContent here"),
    pn.pane.Markdown("## Right Panel\nMore content"),
    sizes=(50, 50),  # Equal sizing initially
    min_size=100,     # Minimum 100px for each panel
    show_buttons=True
)

split.servable()
```

## Usage Examples

### Basic Horizontal Split

```python
import panel as pn
from panel_splitjs import HSplit

pn.extension()

left_panel = pn.Column(
    "# Main Content",
    pn.widgets.TextInput(name="Input"),
    pn.pane.Markdown("This is the main content area.")
)

right_panel = pn.Column(
    "# Sidebar",
    pn.widgets.Select(name="Options", options=["A", "B", "C"]),
)

split = HSplit(
    left_panel,
    right_panel,
    sizes=(70, 30),  # 70% left, 30% right
    min_size=200,    # Minimum 200px for each panel
    show_buttons=True
)

split.servable()
```

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
    sizes=(60, 40),
    min_size=150
)

split.servable()
```

### Collapsible Sidebar

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Start with right panel collapsed
split = Split(
    pn.pane.Markdown("## Main Content"),
    pn.pane.Markdown("## Collapsible Sidebar"),
    collapsed=1,  # 0 for first panel, 1 for second panel, None for not collapsed
    expanded_sizes=(65, 35),  # When expanded, 65% main, 35% sidebar
    show_buttons=True,
    min_size=(200, 200)  # Minimum 200px for each panel
)

# Toggle collapse programmatically
button = pn.widgets.Button(name="Toggle Sidebar")
def toggle(event):
    split.collapsed = None if split.collapsed == 1 else 1
button.on_click(toggle)

pn.Column(button, split).servable()
```

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
    orientation="horizontal"
)

multi.servable()
```

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
- `show_buttons` (bool, default=True): Show collapse/expand toggle buttons on the divider
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

chat = pn.chat.ChatInterface()
output = pn.Column("# Output Area")

split = Split(
    chat,
    output,
    collapsed=None,  # Both panels visible
    expanded_sizes=(50, 50),
    show_buttons=True,
    min_size=(300, 300)  # Minimum 300px for each panel
)

split.servable()
```

### Dashboard with Collapsible Controls

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

controls = pn.Column(
    pn.widgets.Select(name="Dataset", options=["A", "B", "C"]),
    pn.widgets.IntSlider(name="Threshold", start=0, end=100),
    pn.widgets.Button(name="Update")
)

visualization = pn.pane.Markdown("## Main Visualization Area")

split = Split(
    controls,
    visualization,
    collapsed=0,  # Start with controls collapsed
    expanded_sizes=(25, 75),
    show_buttons=True,
    min_size=(250, 400)  # Minimum sizes for each panel
)

split.servable()
```

### Responsive Layout with Size Constraints

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

split = Split(
    pn.pane.Markdown("## Panel 1\nResponsive content"),
    pn.pane.Markdown("## Panel 2\nMore responsive content"),
    sizes=(50, 50),
    min_size=200,        # Minimum 200px per panel
    max_size=800,        # Maximum 800px per panel
    snap_size=50,        # Snap to min size when within 50px
    show_buttons=True
)

split.servable()
```

### Complex Multi-Panel Layout

```python
import panel as pn
from panel_splitjs import MultiSplit

pn.extension()

# Create a four-panel layout
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
    orientation="horizontal"
)

multi.servable()
```

### Nested Splits

```python
import panel as pn
from panel_splitjs import HSplit, VSplit

pn.extension()

# Create a nested layout: horizontal split with vertical split on right
left = pn.pane.Markdown("## Left Panel")

# Right side has a vertical split
top_right = pn.pane.Markdown("## Top Right")
bottom_right = pn.pane.Markdown("## Bottom Right")
right = VSplit(top_right, bottom_right, sizes=(60, 40))

# Main horizontal split
layout = HSplit(
    left,
    right,
    sizes=(30, 70),
    min_size=200
)

layout.servable()
```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.
