import importlib.metadata
import pathlib

import anywidget
import traitlets
import marimo as mo

try:
    __version__ = importlib.metadata.version("graph_widget")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

# repulsion_slider = mo.ui.slider(
#     start=-200, stop=10000, step=10, value=1, debounce=False, label="Repulsion"
# )
# node_scale_slider = mo.ui.slider(
#     start=1, stop=500, step=1, value=20, debounce=True, label="Node scale"
# )
# colour_feature_dropdown = mo.ui.dropdown(
#     options=["None"], value="None", label="Colour by"
# )


class ForceGraphWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    data = traitlets.Dict().tag(sync=True)
    repulsion = traitlets.Int().tag(sync=True)
    node_scale = traitlets.Int().tag(sync=True)
    colour_feature = traitlets.Unicode().tag(sync=True)
    selected_ids = traitlets.List([]).tag(sync=True)
