from dash import html, dcc
from utils.css import ex_stylesheet
import dash_cytoscape as cyto
import os
import json
from dotenv import load_dotenv
import dash_ag_grid as dag
import dash_bootstrap_components as dbc


load_dotenv()

root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")

with open(os.path.join(root_dir,'src/sbmlData/lipid_pathway_map.json'), 'r') as file:
    # Load the JSON data
    lipid_map = json.load(file)

lipids = [{'label': lipid.strip(), 'value': lipid.strip()} for lipid in sorted(lipid_map.keys())]

console1_layout = html.Div([
    html.Div([
        # Header Section
        # near top of console1_layout children
        dcc.Store(id="cy-elements-store",data=None,storage_type="memory"),
        dcc.Store(id="current-lipid-store", data=None, storage_type='memory'),
        
        dcc.Download(id={'type': 'download-target-json', 'index': 'console-1'}),
        dcc.Download(id={'type': 'download-target-csv', 'index': 'console-1'}),
        
        html.Div([
            html.Div([
                html.Span("Lipid Pathways Network Exploration",
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
                        [html.I(className="fa-solid fa-image"), html.Span("Export SVG", className="btn-text")],
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
                    )
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
            
            html.Button(
                html.I(className="fa-solid fa-refresh"),
                id='reset-btn-1',
                className='primary-btn',
                title = 'Recenter graph',
                n_clicks=0,
                style={
                    'fontSize' : '16px',
                    'height' : '30px',
                    'display' : 'inline-flex',
                    'alignItems' : 'center',
                    'justifyContent' : 'center' 
                },
            ),
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

                html.Button('Fetch Network',
                            id='fetch-network-button',
                            className='primary-btn',
                            n_clicks=0,
                            style={'width' : '100%'}
                            ),

                html.Hr(style={'border': '1px solid #EEEEEE', 'margin': '15px 0'}),
                
                html.Div([

                    html.Div(
                        "Highlight Lipid Centric Pathways",
                        className="section-title"
                    ),

                    dcc.Dropdown(
                        id="main-chain-lipid-dropdown",
                        options=[],
                        multi = True,
                        placeholder="Select target lipids...",
                        disabled=False,
                        className="mode-dropdown",
                        
                    ),

                    dbc.RadioItems(
                        id="highlight-radio",
                        className="btn-group network-mode-toggle",
                        inputClassName="btn-check",
                        labelClassName="btn mode-btn",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Full Network", "value": 1, "disabled": True},
                            {"label": "Main Chain", "value": 2, "disabled": True},
                        ],
                        value=1,
                        style={'width' : '100%',
                               'display' : 'flex',
                               'justifyContent' : 'center',
                               'marginTop' : '10px'}
                    ),
                    
                    dbc.Alert("To modify your target lipid or Fetch New Network, above selection should be in Full Network mode",color="info",
                              style= {'padding' : '6px', 'marginTop' : '12px','fontSize' : '13px'})
                    

                ], className="mode-card")
                
            ],
            style={
                'gridColumn': '1',
                'padding': '10px',
                'backgroundColor': "#2e2e2e",
                'fontSize': '14px',
                'overflowY': 'auto',
                'height' : '70vh',
                'scrollbarWidth': 'thin',
                'scrollbarColor': '#555 #2e2e2e'
            }),

            # Cytoscape Graph
            cyto.Cytoscape(
                id={'type': 'cy-graph','index':'console-1'},
                layout={'name': 'cose-bilkent'},
                style={
                    'width': '100%',
                    'height': '70vh',
                    'backgroundColor': "#F3F3F3",
                    'borderRadius' : '10px',
                    'gridColumn': '2'
                },
                elements=[],
                stylesheet=ex_stylesheet,
                minZoom=0.1,
                maxZoom=10
            ),
        ],
        style={
            'display': 'grid',
            # 'height' : '80vh',
            'gridTemplateColumns': '22% 78%',
            'backgroundColor': '#292929'
        })
    ],
    style={
        'border': '1px solid #374152',
        'borderRadius': '10px',
        'backgroundColor': '#292929',
        'boxShadow': ' 2px 3px 4px 0 rgba(0, 0, 0, 0.3)'}

    ),
    
    html.Div([
        html.Button(
            [html.I(className="fa-solid fa-file-csv"), html.Span("Export CSV", className="btn-text")],
            id={'type': 'download-csv-btn', 'index': 'console-1'},
            n_clicks=0,
            className='download-action btn-csv',
            title="Export Table CSV"
        )],
        style={'width' : '100%','marginTop' : '20px','display' :'flex','flexDirection' :'row-reverse'}
    ),
    
    html.Div([
        dag.AgGrid(
            id={'type': 'info-table', 'index': 'console-1'},

            columnDefs=[],   # populated dynamically
            rowData=[],

            defaultColDef={
                # "sortable": True,
                "filter": True,
                "resizable": True,
                "floatingFilter": True,
                "wrapText": True,
                "autoHeight": True,
            },

            dashGridOptions={
                "pagination": True,
                "paginationPageSize": 10,
                "paginationPageSizeSelector": [10, 20, 50, 100],
                "animateRows": True,
                "domLayout": "normal",
            },

            className="ag-theme-alpine-dark",  
            style={
                "height": "350px",
                "width": "100%",
                # "marginTop": "10px"
            },
        )
    ], style={'marginTop' : '20px'})
    
], style={'overflow': 'hidden','margin' : '20px'})

