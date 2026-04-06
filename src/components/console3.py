from dash import html, dcc, dash_table
from utils.css import ex_stylesheet
import dash_cytoscape as cyto
import os
import json
import pickle
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

from dotenv import load_dotenv


load_dotenv()
root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")

with open(os.path.join(root_dir,'src/sbmlData/pathwayDropdownOptions.json'), 'r') as file:
    dropdownOptions = json.load(file)
    physiologicalSystemOptions = dropdownOptions["physiologicalOptions"]

with open(os.path.join(root_dir,"src/sbmlData/targetGene.pkl"), "rb") as f:
    enzymaticGene = pickle.load(f)

enzymaticGene_options = [{'label': gene.strip(), 'value': gene.strip()} for gene in sorted(enzymaticGene)]

console3_layout = html.Div([

    html.Div([
        dcc.Download(id={'type': 'download-target-json', 'index': 'console-3'}),
        dcc.Download(id={'type': 'download-target-csv', 'index': 'console-3'}),

        # Header Section
        html.Div([
            html.Div([
                html.Span("Enzyme-TF regulatory Network",
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
                        id={'type':"download-png-btn", 'index': 'console-3'},
                        n_clicks=0,
                        className='download-action btn-png',
                        title="Export Graph PNG"
                    ),
                    html.Button(
                        [html.I(className="fa-solid fa-file-code"), html.Span("Export JSON", className="btn-text")],
                        id={'type': 'download-json-btn', 'index': 'console-3'},
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
                id='reset-btn-3',
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
            html.Div([
                # --- Gene selection section ---
                html.Div([
                    html.Label("Select Gene(s) to View TFs:",
                            style={'color': '#f1f1f1', 'fontWeight': '600', 'fontSize': '13px'}),
                    dcc.Dropdown(
                        id='gene-dropdown',
                        options=enzymaticGene_options, # type: ignore
                        multi=True, closeOnSelect=False,
                        placeholder='Select Genes...',
                        style={
                            'width': '100%', 'marginBottom': '12px',
                            'backgroundColor': '#fff', 'color': '#000', 'borderRadius': '4px',
                            'scrollbarWidth': 'thin',
                            'scrollbarColor': '#555 #fff'
                        }
                    ),
                    html.Button(
                        'Fetch TFs',
                        id='fetch-tfs-button',
                        className='primary-btn',
                        style={
                            'width': '100%'
                        }
                    )
                ], style={
                    'padding': '8px 10px',
                    # 'borderBottom': '1px solid #444'
                }),

                html.Hr(style={'border': '1px solid #EEEEEE', 'margin': '0px 12px'}),
                
                # --- Filters section ---
                html.Div([
                    html.Div("Filter TFs by:", 
                        style={
                            'color': '#bbb', 'fontSize': '12px',
                            'letterSpacing': '0.5px',
                            'marginBottom': '6px',
                            'borderBottom': '1px solid #3a3a3a',
                            'paddingBottom': '3px'
                        }),
                    html.Label("Physiological System:",
                            style={'color': '#f1f1f1', 'fontWeight': '600', 'fontSize': '13px'}),
                    dcc.Dropdown(
                        id='physiological-systems-dropdown',
                        options=[{'label': key, 'value': key} for key in physiologicalSystemOptions],
                        multi=True, closeOnSelect=False, placeholder='Select Systems...',
                        style={
                            'width': '100%', 'marginBottom': '10px',
                            'backgroundColor': '#fff', 'color': '#000', 'borderRadius': '4px',
                            'scrollbarWidth': 'thin',
                            'scrollbarColor': '#555 #fff'
                        }
                    ),
                    
                    html.Label("Confidence:",
                            style={'color': '#f1f1f1', 'fontWeight': '600', 'fontSize': '13px'}),
                    dbc.RadioItems(
                        id="physio-radio",
                        className="btn-group network-mode-toggle",
                        inputClassName="btn-check",
                        labelClassName="btn mode-btn",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "All", "value": 1, "disabled": True},
                            {"label": "Medium", "value": 2, "disabled": True},
                            {"label": "High", "value": 3, "disabled": True},
                        ],
                        value=1,
                        style={'width' : '100%',
                               'display' : 'flex',
                               'justifyContent' : 'center',
                               'marginTop' : '10px'}
                    ),
                    
                    html.Label("Tissue(s):",
                            style={'color': '#f1f1f1', 'fontWeight': '600', 'fontSize': '13px'}),
                    dcc.Dropdown(
                        id='tissue-dropdown',
                        options=[{'label': 'Select a System to View Tissues', 'value': 'null'}],
                        multi=True, closeOnSelect=False, placeholder='Select Tissues...',
                        style={
                            'width': '100%', 'marginBottom': '10px',
                            'backgroundColor': '#fff', 'color': '#000', 'borderRadius': '4px'
                        }
                    ),
                    
                    html.Label("Confidence:",
                            style={'color': '#f1f1f1', 'fontWeight': '600', 'fontSize': '13px'}),
                    dbc.RadioItems(
                        id="tissue-radio",
                        className="btn-group network-mode-toggle",
                        inputClassName="btn-check",
                        labelClassName="btn mode-btn",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "All", "value": 1, "disabled": True},
                            {"label": "Medium", "value": 2, "disabled": True},
                            {"label": "High", "value": 3, "disabled": True},
                        ],
                        value=1,
                        style={'width' : '100%',
                               'display' : 'flex',
                               'justifyContent' : 'center',
                               'marginTop' : '10px'}
                    ),
                    
                ], style={
                    'padding': '8px 10px',
                    # 'borderBottom': '1px solid #444',
                })
                
            ], 
            style={
                'gridColumn': '1',
                'backgroundColor': '#2e2e2e',
                'fontSize': '14px',
                'overflowY': 'auto',
                'height': '70vh',
                'scrollbarWidth': 'thin',
                'scrollbarColor': '#555 #2e2e2e'
            }),
            
            cyto.Cytoscape(
                id={'type': 'cy-graph','index':'console-3'},
                layout={'name': 'cose-bilkent'},
                style={
                    'width': '100%',
                    'height': '70vh',
                    'backgroundColor': '#F3F3F3',
                    'borderRadius': '10px',
                    'marginBottom': '6px',
                    'gridColumn' : 2
                },
                elements=[],
                stylesheet=ex_stylesheet,
                minZoom=0.1,
                maxZoom=10
            ),
        ],
        style={
            'display': 'grid',
            'gridTemplateColumns': '22% 78%',
            'height' : '70vh',
            'backgroundColor': '#292929',
        })
    ], style={
        'border': '1px solid #374152',
        'borderRadius': '10px',
        'backgroundColor': '#292929',
        'boxShadow': '2px 3px 4px 0 rgba(0, 0, 0, 0.3)'
    }),
    
    html.Div([
        html.Button(
            [html.I(className="fa-solid fa-file-csv"), html.Span("Export CSV", className="btn-text")],
            id={'type': 'download-csv-btn', 'index': 'console-3'},
            n_clicks=0,
            className='download-action btn-csv',
            title="Export Table CSV"
        )],
        style={'width' : '100%','marginTop' : '20px','display' :'flex','flexDirection' :'row-reverse'}
    ),

    html.Div([
        dag.AgGrid(
            id={'type': 'info-table', 'index': 'console-3'},

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
                "enableBrowserTooltips": True,
                # "allowContextMenuWithControlKey": True,
                # "rowSelection": {"mode": "disabled"},
                "tooltipShowDelay": 100,
            },

            className="ag-theme-alpine-dark", 
            style={
                "height": "500px",
                "width": "100%",
            },
        )
    ], style={'marginTop' : '20px'})
], style={'overflow': 'hidden','margin' : '20px'})