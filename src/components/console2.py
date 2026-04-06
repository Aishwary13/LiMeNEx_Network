from dash import html, dcc
from utils.css import ex_stylesheet
import dash_cytoscape as cyto
import os
import dash_ag_grid as dag
import pickle

from dotenv import load_dotenv


load_dotenv()
root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")

with open(os.path.join(root_dir,"src/sbmlData/targetGene.pkl"), "rb") as f:
    enzymaticGene = pickle.load(f)

enzymaticGene_options = [{'label': gene.strip(), 'value': gene.strip()} for gene in sorted(enzymaticGene)]

console2_layout = html.Div([

    html.Div([
        dcc.Download(id={'type': 'download-target-json', 'index': 'console-2'}),
        dcc.Download(id={'type': 'download-target-csv', 'index': 'console-2'}),
        
        # Header Section
        html.Div([
            html.Div([
                html.Span("Lipid-enzyme Reactions",
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
                        id={'type':"download-png-btn", 'index': 'console-2'},
                        n_clicks=0,
                        className='download-action btn-png',
                        title="Export Graph PNG"
                    ),
                    html.Button(
                        [html.I(className="fa-solid fa-file-code"), html.Span("Export JSON", className="btn-text")],
                        id={'type': 'download-json-btn', 'index': 'console-2'},
                        n_clicks=0,
                        className='download-action btn-json',
                        title="Export Graph JSON"
                    )
                ],
                    className='download-panel', 
                    role='group',
                    **{'aria-hidden': 'true'} # type: ignore
                )
            ],
            className='download-container',
            style={
                'position' : 'relative',
                'display' : 'flex',  
            }),
            
            html.Button(
                html.I(className="fa-solid fa-refresh"),
                id='reset-btn-2',
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


        html.Div([
            html.Div([
                html.Label("Select enzymatic gene",
                        style={'color': 'white', 'fontWeight': 'bold', 'marginBottom': '5px'}),

                dcc.Dropdown(
                    id='gene-rxn-dropdown',
                    options=enzymaticGene_options, # type: ignore
                    multi=True,
                    placeholder='Select Genes...',
                    closeOnSelect=False,
                    searchable=True,
                    style={
                        'width': '100%', 'marginBottom': '12px',
                        'backgroundColor': '#fff', 'color': '#000', 'borderRadius': '4px',
                        'scrollbarWidth': 'thin',
                        'scrollbarColor': '#555 #fff'
                    }
                ),

                html.Button('Fetch Reactions',
                            id='fetch-reactions-button',
                            className='primary-btn',
                            style={'width': '100%'}),

                html.Hr(style={'border': '1px solid #EEEEEE', 'margin': '15px 0'}),

            ],
            style={
                'gridColumn': '1',
                'padding': '10px',
                'backgroundColor': "#2e2e2e",
                'fontSize': '14px',
                'overflowY': 'auto',
                'height' : '70vh',
                'scrollbarWidth': 'thin',
                'scrollbarColor': '#555 #2e2e2e',
                # 'borderRight': '2px solid #5e5e5e'
                'borderRadius': '10px',
            }),
            
            html.Div([
                cyto.Cytoscape(
                    id={'type': 'cy-graph','index':'console-2'},
                    layout={'name': 'cose-bilkent'},
                    style={
                        'width': '100%',
                        'height': '70vh',
                        'backgroundColor': '#F3F3F3',
                        'borderRadius': '8px',
                    },
                    elements=[], 
                    stylesheet=ex_stylesheet,
                    minZoom=0.1,
                    maxZoom=10
                ),
                
                html.Div([
                    # Close button stays in DOM permanently (initially hidden via CSS)
                    html.Button(
                        "×",
                        id='cytoscape-pop-close-btn',
                        className='pop-close-btn',
                        title='Close',
                        n_clicks=0
                    ),

                    # Preformatted area for JSON/text (server writes here)
                    html.Pre(
                        id='cytoscape-pop-pre',
                        children='',
                        className='pop-content-pre'
                    )
                ],
                id='cytoscape-tap-edge-data-output',
                className='cytoscape-tap-edge-data-output',
                # keep default hidden here; server will set display:block when showing
                style={
                    'display': 'none',
                    'position': 'absolute',
                    'top': '15px',
                    'right': '15px',
                    'zIndex': 2000
                })
                
            ],style={
                'position' : 'relative',
                'gridColumn': '2',
                'height': '60vh'
            })
            
        ], style={
            'display': 'grid',
            'gridTemplateColumns': '22% 78%',
            'backgroundColor': '#292929',
            'height': '70vh',
            'borderRadius': '10px',
        })
    
    ],
    style={
        'border': '1px solid #374152',
        'borderRadius': '10px',
        'backgroundColor': '#292929',
        'boxShadow': ' 2px 3px 4px 0 rgba(0, 0, 0, 0.3)',
    }),

    html.Div([
        html.Button(
            [html.I(className="fa-solid fa-file-csv"), html.Span("Export CSV", className="btn-text")],
            id={'type': 'download-csv-btn', 'index': 'console-2'},
            n_clicks=0,
            className='download-action btn-csv',
            title="Export Table CSV"
        )],
        style={'width' : '100%','marginTop' : '20px','display' :'flex','flexDirection' :'row-reverse'}
    ),
    
    html.Div([
        dag.AgGrid(
            id={'type': 'info-table', 'index': 'console-2'},

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

            className="ag-theme-alpine-dark",   # ✅ DARK PROFESSIONAL
            style={
                "height": "350px",
                "width": "100%",
                # "marginTop": "10px"
            },
        )
    ], style={'marginTop' : '20px'})
    
], style={'overflow': 'hidden','margin' : '20px'})