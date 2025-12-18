import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_cytoscape as cyto
from utils.css import home_page_new_cytoscape_stylesheet
from utils.home_utils import new_elements

external_js_lib = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"

dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                     external_scripts=[external_js_lib], title="LiMeNex")


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
            # "cursor": "pointer",
            'border': '1px solid #374152'
        }
    )
    
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------- 

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

home_flowchart = html.Div(
    [
        html.Div(
            "NETWORK COMPLEXITY",
            className="home-grpah-header",
        ),
        cyto.Cytoscape(
            id="homepage-flowchart",
            zoomingEnabled=False,
            userZoomingEnabled=False,
            panningEnabled=False,
            userPanningEnabled=False,
            # boxSelectionEnabled=False,
            autounselectify = True,
            style={
                "minWidth": "700px", 
                # "width": "100%",
                "width": "700px",
                "height": "475px",
                "backgroundColor": "#0f0f0f",
                "margin": "0 auto",
                # "border":"1px",
                # "borderColor":"white"
                # "border": "2px solid #4ca9ff",
                
            },
            layout={"name": "preset"},  # preset requires manual (x,y)
            elements = new_elements,
            stylesheet= home_page_new_cytoscape_stylesheet
        ),
],
    style={
        "display" : "flex",
        "flexDirection" : "column",
        "padding" : "50px",
        "width": "100%",
        "overflowX": "auto",  
        # "display": "flex",
        "justifyContent": "center",
        "alignItems" : "center",
        "backgroundColor": "#0f0f0f"
    }
)
    

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------



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
            "LiMeNEx is a powerful platform for visual exploration of lipid metabolic networks, metabolite-protein interactions, and regulating factors of lipids in biological systems with precision and clarity.",
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
                href="Tutorial",
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
    
    # sankey_layout,
    
    home_flowchart,
    
    
    
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
        "padding": "20px 0",
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
            'marginTop': '50px'
    })

],
style={
    "backgroundColor": "#101010"
})

