# graph_widget
An anywidget implementation of force-graph (https://github.com/vasturiano/force-graph). It includes a brush (Cmd-drag).


## Installation

```sh
pip install graph_widget
```

or with [uv](https://github.com/astral-sh/uv):

```sh
uv add graph_widget
```

## Example
An example marimo script (available as `example.py` => run with `uv run marimo edit example.py`):

```python
import graph_widget
import pandas as pd
import json
import requests

url = "https://raw.githubusercontent.com/observablehq/sample-datasets/refs/heads/main/miserables.json"
response = requests.get(url)
data = response.json()

repulsion_slider = mo.ui.slider(
    start=-200, stop=10000, step=10, value=1, debounce=False, label="Repulsion"
)
node_scale_slider = mo.ui.slider(
    start=1, stop=500, step=1, value=20, debounce=True, label="Node scale"
)

data_graph = mo.ui.anywidget(
    graph_widget.ForceGraphWidget(
        data=data,
        repulsion=repulsion_slider.value,
        node_scale=node_scale_slider.value
    )
)

mo.hstack([ data_graph,
            mo.vstack([
                repulsion_slider,
                node_scale_slider])])

selected = data_graph.selected_ids
```

## Development

We recommend using [uv](https://github.com/astral-sh/uv) for development.
It will automatically manage virtual environments and dependencies for you.

```sh
uv run marimo edit example.py
```

Changes made in `src/graph_widget/static/` will be reflected in the notebook.
