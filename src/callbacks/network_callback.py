import time
from dash import MATCH, dcc, callback, Input, Output, State, no_update,ctx
import os
import json
from utils.network_utils import create_nodes_and_edges, processElements, build_dataframe, highlight_elements, remove_highlight, populate_table
import pandas as pd
from itertools import chain
import dash

from dotenv import load_dotenv
load_dotenv()


from callbacks.network_explorer_callbacks import console1, console2, console3


################################################### download callbacks###################################################

@callback(
    Output("warning-modal", "is_open"),
    Output("modal-text", "children"),
    Input("Modal-store", "data"),
    State("warning-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(data, is_open):
    if data:
        return not is_open, data

    return False, ""



@callback(
    Output({'type': 'download-target-json', 'index': MATCH}, 'data'),
    Input({'type': 'download-json-btn', 'index': MATCH}, 'n_clicks'),
    State({'type': 'cy-graph', 'index': MATCH}, 'elements'),
    prevent_initial_call=True,
)
def download_graph_json(n_clicks, elements):
    if n_clicks is None or not elements:
        return dash.no_update,"console is Empty"

    payload = json.dumps(elements, indent=2)

    return dcc.send_bytes(
        lambda buffer: buffer.write(payload.encode("utf-8")),
        filename="graph_elements.json"
    )


@callback(
    Output({'type': 'cy-graph', 'index': MATCH}, 'generateImage'),
    Input({'type': 'download-png-btn', 'index': MATCH}, 'n_clicks'),
    State({'type': 'cy-graph', 'index': MATCH}, 'layout'),
    prevent_initial_call=True,
)
def trigger_image_export(png_clicks, layout):
    """
    This sets generateImage on the cytoscape with the desired format and action.
    For png/jpg we use action='download' (or 'store' if you want imageData populated).
    For svg we use action='download' (SVG is usually downloaded directly).
    """
    # Determine which button triggered this callback
    triggered = ctx.triggered_id  # pattern id object or None
    if not triggered:
        raise dash.exceptions.PreventUpdate

    ftype = 'svg'
    action = 'download' 

    # Optionally compute width/height based on layout or other state
    # e.g. width=1600, height=1200 for high-res png
    image_opts = {
        'type': ftype,
        'action': action
    }

    # If you want specific size for raster formats:
    # if ftype in ('png','jpg'):
    #     image_opts.update({'scale': 2, 'background': 'white', 'width': 1600, 'height': 1200})

    return image_opts


@callback(
    Output({'type': 'download-target-csv', 'index': MATCH}, 'data'),
    Input({'type': 'download-csv-btn', 'index': MATCH}, 'n_clicks'),
    State({'type': 'info-table', 'index': MATCH}, 'virtualRowData'),
    prevent_initial_call=True
)
def download_table_csv(n_clicks, virtual_data):

    if not virtual_data:
        raise dash.exceptions.PreventUpdate

    df = pd.DataFrame(virtual_data)

    filename = f"table_export_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv"

    return dcc.send_data_frame(
        df.to_csv,
        filename,
        index=False
    )