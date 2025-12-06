from dash import html, dcc, dash_table
from utils.css import ex_stylesheet
import dash_cytoscape as cyto
import os
import json
from dotenv import load_dotenv


load_dotenv()

root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")

with open(os.path.join(root_dir,'src/sbmlData/lipid_pathway_map.json'), 'r') as file:
    # Load the JSON data
    lipid_map = json.load(file)

lipids = [{'label': lipid.strip(), 'value': lipid.strip()} for lipid in sorted(lipid_map.keys())]

console1_layout = html.Div([
        # Header Section
        # near top of console1_layout children
        dcc.Download(id={'type': 'download-target-json', 'index': 'console-1'}),
        
        html.Div([
            html.Div([
                html.Span("Console-1: Lipid Pathways Network Exploration",
                        style={'color': 'white', 'fontSize': '16px', 'fontWeight': 'bold'}),

                html.Span("Active",
                    style={
                        'backgroundColor': '#00FF7F',
                        'color': '#000',
                        'fontWeight': '600',
                        'fontSize': '10px',
                        'borderRadius': '10px',
                        'padding': '2px 8px',
                        'marginLeft': '10px',
                        'boxShadow': '0 0 6px #00FF7F'
                    }),
            ],
            style={
                'display' : 'flex',
                'alignItems' : 'center'
            }),
            
            html.Div(style={'flex' : '1'}),
            
            html.Div([
                html.Button(
                    html.I(className="fa-solid fa-download"),
                    id='download-toggle-btn',
                    n_clicks=0,
                    className='download-icon-btn',
                    title='Downloads',
                    **{'aria-label': 'Downloads'} # type: ignore
                ),
                
                html.Div([
                    html.Button(
                        [html.I(className="fa-solid fa-image"), html.Span("Export PNG", className="btn-text")],
                        id={'type':"download-png-btn", 'index': 'console-1'},
                        n_clicks=0,
                        className='download-action btn-png',
                        title="Export Graph PNG"
                    ),
                    html.Button(
                        [html.I(className="fa-solid fa-file-code"), html.Span("Export JSON", className="btn-text")],
                        id={'type':'download-json-btn','index':'console-1'},
                        n_clicks=0,
                        className='download-action btn-json',
                        title="Export Graph JSON"
                    ),
                ],
                    className='download-panel', 
                    role='group',
                )
            ],
            className='download-container',
            style={
                'position' : 'relative',
                'display' : 'flex',  
            }),
        ],
        style={
            'display': 'flex',
            'alignItems': 'center',
            'padding': '8px',
            'borderBottom': '2px solid #333'
        }),


        # Grid: Left Controls + Graph
        html.Div([
            # Left Control Panel
            html.Div([
                html.Label("Search and select Lipids:",
                        style={'color': 'white', 'fontWeight': 'bold', 'marginBottom': '5px'}),

                dcc.Dropdown(
                    id='lipid-dropdown',
                    options=lipids, # type: ignore
                    multi=True,
                    placeholder='Select Lipids...',
                    closeOnSelect=False,
                    searchable=True,
                    maxHeight=150,
                    optionHeight=45,
                    style={
                        'width': '100%',
                        'marginBottom': '10px',
                        'backgroundColor': '#FFFFFF',
                        'color': '#000000',
                        'borderRadius': '4px',
                        'scrollbarWidth': 'thin',
                        'scrollbarColor': '#555 #fff',
                    },
                    
                ),

                html.Div([ 
                    dcc.Checklist(
                        id='direct-pathway-toggle',
                        options=[{'label': 'Highlight the main reaction chain', 'value': 'highlight'}],
                        value=[],
                        inputStyle={'marginRight': '6px'},
                        labelStyle={'color': 'white', 'fontSize': '13px'}
                    )
                ],
                    style={'marginTop': '10px', 'marginBottom': '15px'}
                ),

                html.Button('Fetch Network',
                            id='fetch-network-button',
                            className='primary-btn',
                            n_clicks=0,
                            style={'width' : '100%'}
                            ),

                html.Hr(style={'border': '1px solid #EEEEEE', 'margin': '15px 0'}),

                html.Div(
                    id='pathway-info-container',
                    
                    children=[
                        html.Div("No lipids selected yet.",
                                style={'color': 'white', 'fontSize': '13px', 'textAlign': 'center'}),                        
                    ],

                    style={
                        'paddingTop': '5px',
                        'overflowY': 'auto',
                        'color': 'white',
                        'fontSize': '13px'
                    }
                )
            ],
                style={
                    'gridColumn': '1',
                    'padding': '10px',
                    'backgroundColor': "#2e2e2e",
                    'fontSize': '14px',
                    'overflowY': 'auto',
                    'height' : '80vh',
                    'scrollbarWidth': 'thin',
                    'scrollbarColor': '#555 #2e2e2e'
                }),

            # Cytoscape Graph
            html.Div([
                cyto.Cytoscape(
                    id={'type': 'cy-graph','index':'console-1'},
                    layout={'name': 'cose-bilkent'},
                    style={
                        'width': '100%',
                        'height': '80vh',
                        'backgroundColor': "#F3F3F3",
                        # 'position': 'relative',
                        'borderRadius' : '10px'
                    },
                    elements=[],
                    stylesheet=ex_stylesheet
                ),
                
                
            ],
            style={
                'position' : 'relative',
                'gridColumn': '2',
                'height': '80vh'
            })
        ],
        style={
            'display': 'grid',
            'gridTemplateColumns': '22% 78%',
            'backgroundColor': '#292929'
        })
    ],
    style={
        'margin': '20px',
        'border': '1px solid #374152',
        'borderRadius': '10px',
        'backgroundColor': '#292929',
        'boxShadow': ' 2px 3px 4px 0 rgba(0, 0, 0, 0.3)',
        'overflow': 'hidden'
})