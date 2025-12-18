import os
from dash import html, dcc
from components import console1,console2,console3
from dotenv import load_dotenv
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from utils.css import legend_stylesheet

load_dotenv()


root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")


legend_elements = [
    #parent Nodes
    {'data': {'id': 'nodesLegend', 'label': 'Nodes Legend'},"classes" : 'parent'},
    {'data': {'id': 'edgeLegend', 'label': 'Edge Legend'},"classes" : 'parent'},

    # Nodes
    {'data': {'id': 'tf', 'label': 'Transcription\nFactor','parent' : 'nodesLegend'}, 
     'classes': 'transcriptionFactorGene',
     "position": {"x":100, "y": 60}
    },
    {'data': {'id': 'ezGene', 'label': 'Enzymatic\nGene','parent' : 'nodesLegend'},
     'classes': 'enzymaticGene',
     "position": {"x":310, "y": 60}
     },
    {'data': {'id': 'lipidMetabolite', 'label': 'Lipid Metabolite','parent' : 'nodesLegend'}, 
     'classes': 'lipidMetabolite',
     "position": {"x":100, "y": 120}
     },

    {'data': {'id': 'nonlipidMetabolite', 'label': 'non-lipid Metabolite','parent' : 'nodesLegend'},
     'classes': 'nonlipidMetabolite',
     "position": {"x":310, "y": 120}
     },
    
    {'data': {'id': 'temp', 'label': 'Reaction Node','parent' : 'nodesLegend'},
     'classes': 'temp',
     "position": {"x":205, "y": 120}
     },

    {'data': {'id': 'querynode', 'label': 'Query Node','parent' : 'nodesLegend'},
     'classes': 'querynode',
     "position": {"x":205, "y": 60}
     },

    {'data': {'id': 'node1', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":40, "y": 200}},
    {'data': {'id': 'node2', 'label': 'product','parent' : 'edgeLegend'}, 'classes': 'dummynode',"position": {"x":160, "y": 200}},
    {'data': {'id': 'node3', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode',"position": {"x":40, "y": 240}},
    {'data': {'id': 'node4', 'label': 'product','parent' : 'edgeLegend'}, 'classes': 'dummynode',"position": {"x":160, "y": 240}},
    
    {'data': {'id': 'node5', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":250, "y": 200}},
    {'data': {'id': 'node6', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":370, "y": 200}},
    {'data': {'id': 'node7', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":250, "y": 240}},
    {'data': {'id': 'node8', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":370, "y": 240}},
    
    {'data': {'id': 'node9', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":145, "y": 280}},
    {'data': {'id': 'node10', 'label': 'reactant','parent' : 'edgeLegend'}, 'classes': 'dummynode', "position": {"x":265, "y": 280}},

    #edges
    {'data': {'source': 'node1', 'target': 'node2', 'label': 'Substrate Edge'}, 'classes': 'sub'},
    {'data': {'source': 'node3', 'target': 'node4', 'label': 'Product Edge'}, 'classes': 'prod'},
    {'data': {'source': 'node5', 'target': 'node6', 'label': 'Modifier Edge'}, 'classes': 'mod'},
    {'data': {'source': 'node7', 'target': 'node8', 'label': 'Regulation Edge'}, 'classes': 'reg'},
    {'data': {'source': 'node9', 'target': 'node10', 'label': 'Directly involved Reactions'}, 'classes': 'dir'}
]

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
    
    html.Div(
        [
            html.Div(
                '◀',
                className='legendArrow',
            ),
            html.Div(
                cyto.Cytoscape(
                    id='cytoscape-legend',
                    zoomingEnabled=False,
                    userZoomingEnabled=False,
                    panningEnabled=False,
                    userPanningEnabled=False,
                    autounselectify = True,
                    elements=legend_elements,
                    layout={'name': 'preset'},
                    style={
                        'width': '450px',  # Fixed width for Cytoscape
                        'height': '330px',
                        'background-color': '#FFFFFF',  # White background for legend
                        'border-radius': '8px',
                        'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.2)',
                    },
                    stylesheet=legend_stylesheet,
                ),
                className='legendContent',  # Add a wrapper around the Cytoscape element
            ),
        ],
        className='legendContainer'
    ),
    
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
               'marginTop': '50px'}
    )

], style={'backgroundColor': "#101010", 'height': '100vh', 'overflow': 'auto'})
