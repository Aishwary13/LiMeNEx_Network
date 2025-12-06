import os
from dash import html, dcc
from components import console1,console2,console3
from dotenv import load_dotenv
import dash_bootstrap_components as dbc

load_dotenv()


root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")

# print(type(lipids))
layout = html.Div([

    dcc.Store(id="Modal-store"),
    
    dbc.Modal(
        [
            dbc.ModalHeader("Warning",style={"padding" : "6px 12px 6px 12px"}),
            dbc.ModalBody(id="modal-text"),
        ],
        id="warning-modal",
        is_open=False,
        backdrop=True,  # dims background
    ),
    
    dcc.Store(id="dummy-output-store"),
    dcc.Store(id="graph-update-flag"),
    # ===== HEADER BAR =====
    html.Div([
        html.H2("Lipid Metabolism Network Explorer",
                style={'color': 'white', 'margin': '0', 'padding': '0 20px', 'flex': '1', 'fontSize': '18px'}),
    ],
    style={
        'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between',
        'backgroundColor': '#292929', 'padding': '8px', 'borderBottom': '1px solid #374152'
    }),
    
    console1.console1_layout,
    console2.console2_layout,
    console3.console3_layout,
    html.Div(
        [
            html.Div("© 2025 LiMeNEx — Ray Lab. All rights reserved.", style={"opacity": 0.6}),
        ],
        style={'position':'relative',
               'bottom':'0px','display' : 'flex',
               'flexDirection':'column',
               'textAlign':'center',
               'justifyContent':'center',
               'left':'0','width':'100%',
               'paddingLeft': '3.8em', 
               'paddingBottom':'10px',
               'color': 'white',
               'marginTop': '20px'}
    )

], style={'backgroundColor': "#101010", 'height': '100vh', 'overflow': 'auto'})
