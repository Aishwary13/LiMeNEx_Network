from dash import html, dcc, dash_table
from utils.css import ex_stylesheet
import dash_cytoscape as cyto
import os
import json
import pickle

from dotenv import load_dotenv


load_dotenv()
root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")

with open(os.path.join(root_dir,"src/sbmlData/targetGene.pkl"), "rb") as f:
    enzymaticGene = pickle.load(f)

enzymaticGene_options = [{'label': gene.strip(), 'value': gene.strip()} for gene in sorted(enzymaticGene)]

console2_layout = html.Div([
    
    dcc.Store(id={'type': 'cy-elements-store', 'index': 'console-2'}, storage_type='memory'),
    dcc.Download(id={'type': 'download-target-json', 'index': 'console-2'}),
    dcc.Download(id={'type': 'download-target-csv', 'index': 'console-2'}),
    
    # Header Section
    html.Div([
        html.Div([
            html.Span("Console-2: Lipid-enzyme Reactions",
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
                ),
                html.Button(
                    [html.I(className="fa-solid fa-file-csv"), html.Span("Export CSV", className="btn-text")],
                    id={'type': 'download-csv-btn', 'index': 'console-2'},
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

    html.Div([
        html.Div([
            html.Div([
                html.Label("Select Gene for visualization:",
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
                            style={'width': '100%', 'backgroundColor': '#fca117',
                                'color': 'white', 'border': 'none', 'padding': '6px',
                                'borderRadius': '4px'}),

                html.Hr(style={'border': '1px solid #EEEEEE', 'margin': '15px 0'}),

            ],
                style={
                    'gridColumn': '1',
                    'padding': '10px',
                    'backgroundColor': "#2e2e2e",
                    'fontSize': '14px',
                    'overflowY': 'auto',
                    'height' : '60vh',
                    'scrollbarWidth': 'thin',
                    'scrollbarColor': '#555 #2e2e2e'
                    # 'borderRight': '2px solid #5e5e5e'
                }),
            
            cyto.Cytoscape(
                id={'type': 'cy-graph','index':'console-2'},
                layout={'name': 'cose-bilkent'},
                style={
                    'width': '100%',
                    'height': '60vh',
                    'backgroundColor': '#F3F3F3',
                    'borderRadius': '8px',
                    'gridColumn': '2',
                },
                elements=[], stylesheet=ex_stylesheet
            ),
        ], style={
            'display': 'grid',
            'gridTemplateColumns': '22% 78%',
            'backgroundColor': '#292929',
            'height': '60vh'
        
        }),
        
        html.Div([
            
            html.Div([
                html.Div(
                    "Reaction Information",
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
                        id={'type': 'info-table', 'index': 'console-2'},
                        columns=[
                            {'name': 'Rxn', 'id': 'Rxn'},
                            {'name': 'Enzymatic Gene', 'id': 'EnzymaticGene'},
                            {'name': 'Reactants', 'id': 'Reactants'},
                            {'name': 'Products', 'id': 'Products'},
                            {'name': 'Pathway', 'id': 'Pathway'},
                        ],
                        data=[],
                        style_table={
                            'height': '30vh',
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
                        sort_action='native',
                        filter_action='native',
                        fixed_rows={'headers': True},
                    )
                ],
                style={
                    'width': '100%',
                    'height': '30vh',
                    'overflow' : 'auto',
                    'boxSizing' : 'border-box',
                })
            ],
            style={
                'display': 'flex',
                'flexDirection' : 'row',
                'gridColumn' : '2',
                'height': '30vh'
            }),
        ], style={
            'backgroundColor': '#2E2E2E',
            'height': '30vh',
            'display': 'grid',
            'gridTemplateColumns': '22% 78%'
        }) 
    ],
    style={
        'backgroundColor': '#292929',
        'height': '90vh'
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