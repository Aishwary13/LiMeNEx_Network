import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, clientside_callback, ClientsideFunction, Input, Output

external_js_lib = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                     external_scripts=[external_js_lib], title="LiMeNex")

# layout = html.Div([
#     # Welcome Section (Hero Section)
#     html.Div([
#         html.H1("Welcome to LiMeNEx: Your Gateway to Lipidomics Research",
#                 style={'color': '#FFFFFF', 'fontWeight': 'bold', 'textAlign': 'center'}),
#         html.P("Explore the intricate network of lipid metabolic pathways and gain insights into gene regulation with advanced differential expression analysis.",
#                style={'color': '#FFFFFF', 'textAlign': 'center', 'maxWidth': '800px', 'margin': '0 auto'}),
#         html.A("Get Started", href="#features",
#                style={'display': 'inline-block', 'padding': '10px 20px', 'backgroundColor': '#4CAF50', 
#                       'color': '#FFFFFF', 'textDecoration': 'none', 'borderRadius': '5px', 
#                       'marginTop': '20px', 'textAlign': 'center'})
#     ], style={'padding': '50px', 'textAlign': 'center'}),

#     # 3D Network Animation Section
#     html.Div([
#         html.H2("Visualize the Lipid Metabolic Pathways", style={'color': '#FFFFFF', 'fontWeight': 'bold', 'textAlign': 'center'}),
#         html.Div(id='network-animation', style={'height': '500px', 'backgroundColor': '#2C2C2C'}),
#         html.P("Explore the interconnected pathways that drive lipid metabolism. Watch as nodes change color to indicate differential expression.",
#                style={'color': '#CCCCCC', 'textAlign': 'center', 'marginTop': '20px'})
#     ], style={'backgroundColor': '#292929', 'padding': '50px 20px'}),

#     # Functionalities Section
#     html.Div([
#         html.H2("Key Features & Functionalities", style={'color': '#FFFFFF', 'fontWeight': 'bold', 'textAlign': 'center'}),
#         html.Ul([
#             html.Li("1. Differential Expression Analysis: Identify upregulated and downregulated genes with precision.", style={'color': '#CCCCCC'}),
#             html.Li("2. Custom Data Input: Upload your data and see real-time results on the network.", style={'color': '#CCCCCC'}),
#             html.Li("3. Interactive Visualization: Interact with the network and explore gene relationships visually.", style={'color': '#CCCCCC'}),
#         ], style={'listStyleType': 'none', 'paddingLeft': '0', 'textAlign': 'left', 'maxWidth': '800px', 'margin': '0 auto', 'textAlign': 'center'})
#     ], style={'backgroundColor': '#1A1A1A', 'padding': '50px 20px'}),

#     # Step-by-Step Guide Section
#     html.Div([
#         html.H2("How to Use LiMeNEx", style={'color': '#FFFFFF', 'fontWeight': 'bold', 'textAlign': 'center'}),
#         html.Div([
#             html.Div([
#                 html.H3("Step 1", style={'color': '#4CAF50', 'textAlign': 'center'}),
#                 html.P("Upload your gene expression data.", style={'color': '#CCCCCC', 'textAlign': 'center'})
#             ], style={'padding': '20px', 'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),

#             html.Div([
#                 html.H3("Step 2", style={'color': '#4CAF50', 'textAlign': 'center'}),
#                 html.P("Run differential expression analysis.", style={'color': '#CCCCCC', 'textAlign': 'center'})
#             ], style={'padding': '20px', 'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),

#             html.Div([
#                 html.H3("Step 3", style={'color': '#4CAF50', 'textAlign': 'center'}),
#                 html.P("Visualize the upregulated and downregulated genes on the network.", style={'color': '#CCCCCC', 'textAlign': 'center'})
#             ], style={'padding': '20px', 'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
#         ], style={'textAlign': 'center'})
#     ], style={'backgroundColor': '#2D2D2D', 'padding': '50px 20px'}),
# ], style={'backgroundColor': '#1A1A1A', 'height': '100vh'})

def make_stat_row(label, value, highlight=False):
    return html.Div([
        html.Span(label, style={"opacity": 0.7}),
        html.Span(
            value,
            style={
                "fontWeight": "600",
                "color": "#4da6ff" if highlight else "white"
            }
        ),
    ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "padding": "6px 0",
            "borderBottom": "1px solid rgba(255,255,255,0.08)"
        })
    

def make_feature_card(icon, icon_color, title, text):
    return html.Div([

        # Icon
        html.Div([
            html.I(className=icon, style={
                "fontSize": "26px",
                "color": icon_color
            })
        ], style={"marginBottom": "12px"}),

        # Title
        html.Div(title, style={
            "color": "white",
            "fontWeight": "700",
            "fontSize": "18px",
            "marginBottom": "8px"
        }),

        # Description
        html.Div(text, style={
            "color": "#cccccc",
            "fontSize": "14px",
            "lineHeight": "1.4"
        })

    ],
        className="feature-card",
        style={
            "backgroundColor": "#1e1e1e",
            "padding": "24px",
            "borderRadius": "12px",
            "width": "300px",
            "boxShadow": "0 6px 12px rgba(55, 65, 82, 0.6)",
            "transition": "transform 0.25s ease, box-shadow 0.25s ease",
            "cursor": "pointer",
            'border': '1px solid #374152'
        }
    )


# ---------- HERO + NETWORK PREVIEW (side-by-side, responsive) ----------
layout = html.Div([
    # html.Div(id="typed-trigger", style={"display": "none"}),
    html.Div([
        
        html.Div([
            html.Div(className="title-halo"),
            html.Div(
                [
                    # these dots are positioned with style dicts for variety
                    html.Div(className="hero-dot", style={'left': '20%', 'top': '18%', 'width': '12px', 'height': '12px', 'background': 'rgba(20,230,255,0.95)', 'animationDuration': '8s'}),
                    html.Div(className="hero-dot", style={'left': '50%', 'top': '8%', 'width': '10px', 'height': '10px', 'background': 'rgba(156,77,255,0.9)', 'animationDuration': '10s'}),
                    html.Div(className="hero-dot", style={'left': '78%', 'top': '28%', 'width': '8px', 'height': '8px', 'background': 'rgba(76,169,255,0.95)', 'animationDuration': '7s'}),
                ],
                className="hero-dots"
            )
        ], style={'position': 'absolute', 'inset': '0', 'pointerEvents': 'none'}),
        
        # html.Img(src='/assets/mini-network.svg',
        #             style={'width': '360px', 'height': '160px', 'display': 'block'}),
    
        # Left: Hero text & CTAs

        html.H1("LiMeNEx",
           style={
                "background": "linear-gradient(90deg, #14e6ff, #4ca9ff, #9c4dff)",
                "WebkitBackgroundClip": "text",
                "WebkitTextFillColor": "transparent",
                "fontSize": "50px",
                "fontWeight": "700",
                "marginBottom": "10px",
            }, 
        ),
        
        html.H2([
            # Li (from Lipid)
            html.Span("Li", className="grad-li"),
            html.Span("pid ", style={"color": "white"}),

            # Me (from Metabolic)
            html.Span("Me", className="grad-me"),
            html.Span("tabolic ", style={"color": "white"}),

            # N (from Network)
            html.Span("N", className="grad-n"),
            html.Span("etwork ", style={"color": "white"}),

            # Ex (from Explorer)
            html.Span("Ex", className="grad-ex"),
            html.Span("plorer", style={"color": "white"}),
        ],
            style={
                "fontSize": "30px",
                "fontWeight": "600",
                "marginBottom": "20px",
            }
        ),

                
        html.P(
            "LiMeNEx is a powerful platform for analyzing and visualizing metabolic networks, protein interactions, and biological pathways with precision and clarity.",
            style={
                "color": "#CFCFCF",
                "maxWidth": "640px",
                "marginBottom": "18px",
                "fontSize": "14px",
                "textAlign": "center",
            },
        ),
        
        html.P("This website is free and open to all users and there is no login requirement.",
            style={
                "color": "#CFCFCF",
                "maxWidth": "640px",
                "marginBottom": "20px",
                "fontSize": "14px",
                "textAlign": "center",
            },
        ),
        
        html.Div([
            html.A(
                "Get Started",
                href="Network2",
                style={
                    "display": "inline-block",
                    "padding": "10px 18px",
                    "backgroundColor": "#0fd3ff",
                    "color": "#061b23",
                    "borderRadius": "8px",
                    "textDecoration": "none",
                    "fontWeight": "600",
                    "fontSize": "15px",
                },
            ),
            html.A(
                "Learn More",
                href="#how-to-use",
                style={
                    "display": "inline-block",
                    "padding": "10px 18px",
                    "backgroundColor": "transparent",
                    "color": "#9ad6ff",
                    "border": "1px solid rgba(157, 205, 255, 0.12)",
                    "borderRadius": "8px",
                    "textDecoration": "none",
                    "fontWeight": "600",
                    "fontSize": "15px",
                },
            ),
        ],
        style={
            "marginTop": "8px",
            "display" : "flex",
            "flex-wrap" : "wrap" ,
            "gap" : "10px",
            "width" : "100%",
            "alignItems": "center",
            "justifyContent": "center",
        }),
    

    ],
    # Layout: two-column responsive grid — stacks on narrow screens
    style={ 
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "margin": "0 auto",
        "padding": "40px 20px 0px 20px",
    }),
    
    html.Div([

        # =========================================================
        # TABLE CARD 1 — NETWORK SUMMARY
        # =========================================================
        html.Div([
            html.Div([
                html.I(className="fa-solid fa-network-wired",
                       style={"marginRight": "8px", "color": "#4da6ff"}),
                html.Span("Network Summary",
                          style={"fontWeight": "600", "fontSize": "16px"})
            ], style={
                # "display": "flex",
                # "alignItems": "center",
                # "marginBottom": "12px"
            }, className="table-header-gradient background1"),

            html.Div([
                make_stat_row("Total Nodes", "12,847"),
                make_stat_row("Total Edges", "45,293"),
                make_stat_row("Network Density", "0.548", highlight=True),
                make_stat_row("Avg. Degree", "7.05"),
                make_stat_row("Clustering Coefficient", "0.421", highlight=True)
            ],style= {"padding" : "20px"})
        ],
        style={
            "backgroundColor": "#202020",
            # "padding": "20px",
            "borderRadius": "12px",
            "boxShadow": "0px 4px 20px rgba(0,0,0,0.35)",
            "width": "450px",
            "color": "white",
            'borderBottom': '2px solid #374152'
        }),

        # =========================================================
        # TABLE CARD 2 — CATEGORY SUMMARY
        # =========================================================
        html.Div([
            html.Div([
                html.I(className="fa-solid fa-flask",
                       style={"marginRight": "8px", "color": "#c57bff"}),
                html.Span("Biological Category Summary",
                          style={"fontWeight": "600", "fontSize": "16px"})
            ], style={
                # "display": "flex",
                # "alignItems": "center",
                # "marginBottom": "12px"
            },className="table-header-gradient background2"),

            html.Div([
                make_stat_row("Metabolic Pathways", "3,421"),
                make_stat_row("Protein Interactions", "5,847"),
                make_stat_row("Gene Regulatory", "2,156", highlight=True),
                make_stat_row("Signal Transduction", "1,423"),
                make_stat_row("Total Categories", "12,847", highlight=True)
            ],style= {"padding" : "20px"})
        ],
        style={
            "backgroundColor": "#202020",
            "borderRadius": "12px",
            "boxShadow": "0px 4px 20px rgba(0,0,0,0.35)",
            "width": "450px",
            "color": "white",
            'borderBottom': '2px solid #374152'
        }),

    ],
    style={
        "display": "flex",
        "justifyContent": "center",
        "marginTop": "40px",
        "padding": "0px 52px 40px 52px",
        "fontSize": "15px",
        "flexWrap": "wrap",
        "gap" : "20px",
    }),
    
    html.Div([

        # Section Title
        html.H2("Key Features", 
                style={
                    "color": "#4da6ff",
                    "fontWeight": "700",
                    "textAlign": "center",
                    "marginBottom": "5px",
                    "fontSize": "32px"
                }),

        html.P("Powerful Webserver for comprehensive biological network analysis",
            style={
                "color": "#cccccc",
                "textAlign": "center",
                "marginBottom": "40px"
            }),

        # FEATURE CARDS GRID
        html.Div([

            make_feature_card(
                icon="fa-solid fa-route",
                icon_color="#28d9d4",
                title="Pathway Exploration",
                text="Navigate lipid metabolism pathways with multi-select options and real-time network visualization."
            ),

            make_feature_card(
                icon="fa-solid fa-dna",
                icon_color="#9e7bff",
                title="Gene & System Analysis",
                text="Explore gene interactions across systems and tissues with automatic transcription factor mapping."
            ),

            make_feature_card(
                icon="fa-solid fa-magnifying-glass",
                icon_color="#d24bff",
                title="Targeted Search",
                text="Search genes, lipids, or transcription factors and instantly visualize them."
            ),

            make_feature_card(
                icon="fa-solid fa-diagram-project",
                icon_color="#00c2ff",
                title="Interactive Networks",
                text="Interact with network and drag nodes to explore relationships and details."
            ),

            make_feature_card(
                icon="fa-solid fa-table",
                icon_color="#4dabff",
                title="Data Tables",
                text="Access detailed tables for genes, TFs, lipids, and pathways with export capabilities."
            ),

            make_feature_card(
                icon="fa-solid fa-arrow-up-from-bracket",
                icon_color="#c07dff",
                title="Export & Share",
                text="Export networks as SVG or in json file and download data tables for offline analysis."
            ),

        ], className="key-features-grid")

    ],
    style={
        "padding": "40px 0",
    }),
    
    
    
    
    
    html.Div([
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
            'marginTop': '20px'
    })

],
style={
    "backgroundColor": "#101010"
})


# clientside_callback(
#     ClientsideFunction(namespace="clientside", function_name="expandSegments"),
#     [
#         Output("seg-li", "children"),
#         Output("seg-me", "children"),
#         Output("seg-n",  "children"),
#         Output("seg-ex", "children"),
#         Output("seg-li", "className"),
#         Output("seg-me", "className"),
#         Output("seg-n",  "className"),
#         Output("seg-ex", "className"),
#         Output("title-interval", "disabled"),   # <- NEW: disable the Interval after expansion
#     ],
#     Input("title-interval", "n_intervals"),
# )

# clientside_callback(
#     ClientsideFunction(namespace="clientside", function_name="initTypedOnce"),
#     Output("typed-trigger", "children"),
#     Input("url", "pathname"),   # fires on initial load / navigation
# )


