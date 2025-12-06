from dash import html, dcc, dash_table
from utils.css import ex_stylesheet
import dash_cytoscape as cyto
import os
import json
import pickle

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
    dcc.Download(id={'type': 'download-target-json', 'index': 'console-3'}),
    dcc.Download(id={'type': 'download-target-csv', 'index': 'console-3'}),

    # Header Section
    html.Div([
        html.Div([
            html.Span("Console-3: Enzyme-TF regulatory Network",
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
                ),
                html.Button(
                    [html.I(className="fa-solid fa-file-csv"), html.Span("Export CSV", className="btn-text")],
                    id={'type': 'download-csv-btn', 'index': 'console-3'},
                    n_clicks=0,
                    className='download-action btn-csv',
                    title="Export Table CSV"
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
                'height': '55vh',
                'gridColumn' : 1,
                'scrollbarWidth': 'thin',
                'scrollbarColor': '#555 #2e2e2e'
            }),
            
            cyto.Cytoscape(
                id={'type': 'cy-graph','index':'console-3'},
                layout={'name': 'cose-bilkent'},
                style={
                    'width': '100%',
                    'height': '55vh',
                    'backgroundColor': '#F3F3F3',
                    'borderRadius': '8px',
                    'marginBottom': '6px',
                    'gridColumn' : 2
                },
                elements=[], stylesheet=ex_stylesheet
            ),
        ],
        style={
            'display': 'grid',
            'gridTemplateColumns': '22% 78%',
            'height' : '55vh'
        }),


        html.Div([
            # TF/Gene selectors + button
            html.Div([
                html.Label("Select Tfs and Enzymatic Gene(s) to View Information:",
                            style={'color': '#f1f1f1', 'fontWeight': '600', 'fontSize': '13px'}),
                dcc.Dropdown(
                    id='tf-select',
                    options=[], placeholder='Select TF(s)...',
                    multi=True, closeOnSelect=False,
                    style={'width': '100%', 'backgroundColor': '#fff', 'color': '#000', 'borderRadius': '4px','marginBottom' : '10px','scrollbarWidth': 'thin',
                        'scrollbarColor': '#555 #fff'}
                ),
                dcc.Dropdown(
                    id='gene-select',
                    options=[], placeholder='Select Gene(s)...',
                    multi=True, closeOnSelect=False,
                    style={'width': '100%', 'backgroundColor': '#fff', 'color': '#000', 'borderRadius': '4px','marginBottom' : '10px','scrollbarWidth': 'thin',
                        'scrollbarColor': '#555 #fff'}
                ),
                html.Button(
                    "Load Evidence",
                    id='load-evidence-btn',
                    className='primary-btn',
                    n_clicks=0,
                    style={
                        'width': '50%'
                    }
                ),
            ], style={'fontSize': '14px','gridColumn': '1',
                        'padding': '8px 10px',
                        'alignItems': 'center',
                        'justifyContent': 'center','overflowY': 'auto','borderTop' : '1px solid #5e5e5e','scrollbarWidth': 'thin','scrollbarColor': '#555 #2e2e2e'}),

            html.Div([
                
                html.Div(
                    "Evidence Table",
                    style={
                        'writingMode': 'vertical-rl',     # Vertical text
                        'transform': 'rotate(180deg)',   # Make text top-to-bottom
                        'color': 'white',
                        # 'fontWeight': 'bold',
                        'padding': '10px 5px',
                        'backgroundColor': '#1f1f1f',
                        'borderLeft': '1px solid #444',
                        'height': '100%',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'fontSize': '14px',
                        'width' : '40px'
                    }
                ),
                
                html.Div([
                    dash_table.DataTable(
                        id={'type': 'info-table', 'index': 'console-3'},
                        columns=[
                            {'name': 'TF', 'id': 'TF'},
                            {'name': 'Target Gene', 'id': 'TargetGene'},
                            {'name': 'Tissue', 'id': 'Tissue'},
                            {'name': 'SPP', 'id': 'Experiment'},
                            {'name': 'Chea', 'id': 'Chea'},
                            {'name': 'Signor', 'id': 'Signor'},
                            {'name': 'Trrust', 'id': 'Trrust'}
                        ],
                        data=[],
                        style_table={
                            'height': '35vh',
                            'overflowY': 'auto',
                            'width': '100%',
                            'overflowX' : 'auto',
                            'boxSizing' : 'border-box'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'padding': '4px 6px',  # reduce vertical padding
                            'whiteSpace': 'normal',
                            'fontSize': '12px',
                        },
                        style_header={
                            'backgroundColor': '#1f1f1f',
                            'fontWeight': '600',
                            'color': 'white',
                            'borderBottom': '1px solid #444'
                        },
                        style_data={
                            'backgroundColor': '#222',
                            'color': 'white'
                        },
                        sort_action='native', filter_action='native',
                        fixed_rows={'headers': True}
                    )
                ],
                style={
                    'width': '100%',
                    'height': '35vh',
                    'overflow' : 'auto',
                    'boxSizing' : 'border-box',
                }),
            ],
            style={
                'display': 'flex',
                'flexDirection' : 'row',
                'gridColumn': '2',
                'height': '35vh'
            })
        ], style={
            'backgroundColor': '#2e2e2e',
            'height': '35vh',
            'display': 'grid',
            'gridTemplateColumns': '22% 78%'
            
        })
            
    ], style={
        'backgroundColor': '#292929',
        'height': '90vh'
    })
], style={
    'margin': '20px',
    'border': '1px solid #374152',
    'borderRadius': '10px',
    'backgroundColor': '#292929',
    'boxShadow': '2px 3px 4px 0 rgba(0, 0, 0, 0.3)',
    'overflow': 'hidden'
})