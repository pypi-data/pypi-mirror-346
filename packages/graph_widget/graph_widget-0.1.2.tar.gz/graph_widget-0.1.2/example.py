import marimo

__generated_with = "0.11.6"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    return mo, pd


@app.cell
def _():
    import graph_widget
    return (graph_widget,)


@app.cell
def _():
    # import json
    # import requests

    # url = "https://raw.githubusercontent.com/observablehq/sample-datasets/refs/heads/main/miserables.json"
    # response = requests.get(url)
    # data = response.json()
    # for item in data["nodes"]:
    #     item["group"] = str(item["group"])
    return


@app.cell
def _():
    # with open('data.json', 'r') as file:
    #     data = json.load(file)
    data = {'nodes':
            [{"id": 1, "kind": "sample"},
            {"id": 2, "kind": "sample"},
            {"id": 3, "kind": "OTU", "degree": 3},
            {"id": 4, "kind": "OTU", "degree": 2},
            {"id": 5, "kind": "OTU", "degree": 3}],
            "links": [
                {"source": 1, "target": 3},
                {"source": 1, "target": 4},
                {"source": 1, "target": 5},
                {"source": 2, "target": 3},
                {"source": 1, "target": 4},
                {"source": 1, "target": 5},
                {"source": 2, "target": 3},
                {"source": 2, "target": 5},
            ]}
    return (data,)


@app.cell
def _(data):
    list(data["nodes"][0].keys())
    return


@app.cell
def _(data, mo):
    repulsion_slider = mo.ui.slider(
        start=-100, stop=500, step=10, value=1, debounce=False, label="Repulsion"
    )
    node_scale_slider = mo.ui.slider(
        start=1, stop=20, step=1, value=3, debounce=True, label="Node scale"
    )
    colour_feature_dropdown = mo.ui.dropdown(
        options=list(data["nodes"][3].keys()), value="kind", label="Colour by"
    )
    return colour_feature_dropdown, node_scale_slider, repulsion_slider


@app.cell
def _(
    colour_feature_dropdown,
    data,
    graph_widget,
    mo,
    node_scale_slider,
    repulsion_slider,
):
    data_graph = mo.ui.anywidget(
        graph_widget.ForceGraphWidget(
            data=data,
            repulsion=repulsion_slider.value,
            node_scale=node_scale_slider.value,
            colour_feature=colour_feature_dropdown.value
        )
    )
    return (data_graph,)


@app.cell
def _(
    colour_feature_dropdown,
    data_graph,
    mo,
    node_scale_slider,
    repulsion_slider,
):
    plot = mo.hstack([data_graph,
                mo.vstack([
                    repulsion_slider,
                    node_scale_slider,
                    colour_feature_dropdown])], justify="start")
    # plot = mo.hstack([data_graph])
    return (plot,)


@app.cell
def _(plot):
    plot
    return


@app.cell
def _(data_graph):
    selected = data_graph.selected_ids
    return (selected,)


@app.cell
def _(selected):
    selected
    return


@app.cell
def _(data, selected):
    filtered_nodes = [node for node in data["nodes"] if node["id"] in selected]
    filtered_nodes
    return (filtered_nodes,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
