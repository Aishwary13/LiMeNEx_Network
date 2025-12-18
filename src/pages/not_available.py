from dash import html
from urllib.parse import parse_qs

def layout(search=""):
    params = parse_qs(search.lstrip("?"))
    node = params.get("node", ["Unknown"])[0]
    node_type = params.get("type", ["Unknown"])[0]

    return html.Div(
        style={
            "height": "100vh",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "backgroundColor": "#f4f6f8",
            "fontFamily": "Arial"
        },
        children=[
            html.Div(
                style={
                    "padding": "35px",
                    "backgroundColor": "white",
                    "borderRadius": "12px",
                    "boxShadow": "0 6px 18px rgba(0,0,0,0.15)",
                    "textAlign": "center",
                    "maxWidth": "550px"
                },
                children=[
                    html.H2("Source Currently Not Available"),
                    html.P(
                        "The selected node does not yet have an associated external resource.",
                        style={"marginTop": "15px"}
                    ),
                    html.Hr(),
                    html.P(f"Node: {node}"),
                    html.P(f"Type: {node_type}"),
                    html.Br(),
                    html.P(
                        "You may safely close this tab.",
                        style={"color": "#666"}
                    )
                ]
            )
        ]
    )
