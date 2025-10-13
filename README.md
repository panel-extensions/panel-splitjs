# panel-splitjs

[![CI](https://img.shields.io/github/actions/workflow/status/panel-extensions/panel-splitjs/ci.yml?style=flat-square&branch=main)](https://github.com/panel-extensions/panel-splitjs/actions/workflows/ci.yml)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/panel-splitjs?logoColor=white&logo=conda-forge&style=flat-square)](https://prefix.dev/channels/conda-forge/packages/panel-splitjs)
[![pypi-version](https://img.shields.io/pypi/v/panel-splitjs.svg?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/panel-splitjs)
[![python-version](https://img.shields.io/pypi/pyversions/panel-splitjs?logoColor=white&logo=python&style=flat-square)](https://pypi.org/project/panel-splitjs)

A responsive, draggable split panel component for [Panel](https://panel.holoviz.org) applications, powered by [split.js](https://split.js.org/).

## Features

- **Draggable divider** - Resize panels by dragging the divider between them
- **Collapsible panels** - Toggle panels open/closed with optional buttons
- **Flexible orientation** - Support for both horizontal and vertical splits
- **Minimum size constraints** - Enforce minimum panel sizes to prevent over-collapse
- **Smooth animations** - Beautiful transitions when toggling panels
- **Customizable sizes** - Control initial and expanded panel sizes
- **Invertible layout** - Swap panel positions and button locations

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
    sizes=(50, 50),  # Equal sizing
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
    orientation="vertical"
)

split.servable()
```

### Collapsible Sidebar

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Start with sidebar collapsed
split = Split(
    pn.pane.Markdown("## Main Content"),
    pn.pane.Markdown("## Collapsible Sidebar"),
    collapsed=True,
    expanded_sizes=(65, 35),  # When expanded, 65% main, 35% sidebar
    show_buttons=True,
    min_sizes=(200, 200)  # Minimum 200px for each panel
)

# Toggle collapse programmatically
button = pn.widgets.Button(name="Toggle Sidebar")
button.on_click(lambda e: setattr(split, 'collapsed', not split.collapsed))

pn.Column(button, split).servable()
```

### Inverted Layout

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Inverted: right panel collapses, button on right side
split = Split(
    pn.pane.Markdown("## Secondary Panel"),
    pn.pane.Markdown("## Main Content"),
    invert=True,  # Swap layout and button position
    collapsed=True,
    expanded_sizes=(35, 65),
    show_buttons=True
)

split.servable()
```

## API Reference

### Split

The main split panel component with full customization options.

**Parameters:**

- `objects` (list): Two Panel components to display in the split panels
- `collapsed` (bool, default=False): Whether the secondary panel is collapsed
- `expanded_sizes` (tuple, default=(50, 50)): Percentage sizes when expanded (must sum to 100)
- `invert` (bool, default=False): Swap panel positions and button locations (constant after init)
- `min_sizes` (tuple, default=(0, 0)): Minimum sizes in pixels for each panel
- `orientation` (str, default="horizontal"): Either "horizontal" or "vertical"
- `show_buttons` (bool, default=False): Show collapse/expand toggle buttons
- `sizes` (tuple, default=(100, 0)): Initial percentage sizes (must sum to 100)

### HSplit

Horizontal split panel (convenience class).

Same parameters as `Split` but `orientation` is locked to "horizontal".

### VSplit

Vertical split panel (convenience class).

Same parameters as `Split` but `orientation` is locked to "vertical".

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
    collapsed=False,
    expanded_sizes=(50, 50),
    show_buttons=True,
    min_sizes=(300, 300)
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
    collapsed=True,
    expanded_sizes=(25, 75),
    show_buttons=True,
    min_sizes=(250, 400)
)

split.servable()
```

### Responsive Layout

```python
import panel as pn
from panel_splitjs import Split

pn.extension()

# Automatically adjust to available space
split = Split(
    pn.pane.Markdown("## Panel 1\nResponsive content"),
    pn.pane.Markdown("## Panel 2\nMore responsive content"),
    sizes=(50, 50),
    min_sizes=(200, 200),  # Prevent panels from getting too small
    show_buttons=True
)

split.servable()
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
