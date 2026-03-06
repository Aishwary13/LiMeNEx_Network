import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import dash_cytoscape as cyto

font_awesome1 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css'
font_awesome3 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/solid.min.css'

external_js_lib="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
local_warn_suppressor = "/assets/ignore_wheel_warn.js"
typedjs = "https://cdn.jsdelivr.net/npm/typed.js@2.0.12"
temp2 = "https://unpkg.com/react@18/umd/react.production.min.js"
temp3 = "https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"


# os.environ['TMPDIR'] = 'C:\\Temp'

# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheManager(cache)

dash_app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,font_awesome1,font_awesome3],
                    title="LiMeNex" ,use_pages=True,suppress_callback_exceptions=True,
                    external_scripts=[external_js_lib, local_warn_suppressor, typedjs, temp2, temp3])

cyto.load_extra_layouts()

server = dash_app.server

from pages import home, contact,network,not_available, tutorial
from callbacks import network_callback
from callbacks.clientside_callbacks import uniprot_and_lipid_redirect_callback, recenter_cytoscape_graph

# dataBasePath= sbml_network.dataBasePath

link_style = {
    'padding': '0.75em 1em',
    'text-decoration': 'none',
    'color': 'white',
    'display': 'block'
}

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div([
        # html.Div(
        #     dcc.Link(f"{page['name']}", href=page["relative_path"], style=link_style)
        # ) for page in dash.page_registry.values()
        html.Div([
                html.Div([
                    html.Img(src="assets/network_pic.png", style={"width": "3rem"}),
                    html.H1("LiMeNEx",
                        style={
                                "background": "linear-gradient(90deg, #14e6ff, #4ca9ff, #9c4dff)",
                                "WebkitBackgroundClip": "text",
                                "WebkitTextFillColor": "transparent",
                                "fontSize": "32px",
                                "fontWeight": "500",
                                "margin": "0px",
                                # "marginBottom": "10px",
                            }, 
                        ),
                    # html.Img(src="assets/Title.png", style={"width": "9rem"})
                    # html.H5("LiMeNEx", style={'color': 'white', 'marginTop': '20px'}),
                    # html.Img(src="assets/Title.png", style={"width": "4.5rem"})
                ], className='image_title')
            ], className="sidebar-header"),
        # html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink([html.Div([
                    html.I(className="fa-solid fa-house"),
                    html.Span("Home", style={'marginTop': '0px', 'marginLeft' :'6px'})], className='icon_title')],
                    href="/",
                    active="exact",
                    className="nav-bar-icons pe-3",
                ),
                dbc.NavLink([html.Div([
                    html.I(className="fa-solid fa-circle-nodes"),
                    html.Span("Network", style={'marginTop': '0px', 'marginLeft' :'6px'})], className='icon_title')],
                    href="/Network2",
                    active="exact",
                    className="pe-3",
                    style={'marginTop' : '7px'}
                ),
                dbc.NavLink([html.Div([
                    html.I(className="fa-solid fa-book"),
                    html.Span("Tutorial", style={'marginTop': '0px', 'marginLeft' :'6px'})], className='icon_title')],
                    href="/Tutorial",
                    active="exact",
                    className="pe-3",
                    style={'marginTop' : '7px'}
                ),
                dbc.NavLink([html.Div([
                    html.I(className="fa-solid fa-address-card"),
                    html.Span("Contact Us", style={'marginTop': '0px', 'marginLeft' :'6px'})], className='icon_title')],
                    href="/Contact",
                    active="exact",
                    className="pe-3",
                    style={'marginTop' : '7px'}
                ),
            ],
            vertical=True,
            pills=True,
            id='nav-links',
            style={'padding':'6px'}
        )

    ], className='sidebar'),

    html.Div(
        # dash.page_container,
        className='page-content',
        id='page-content',
        children=[]
    )
])


@dash_app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
        State('url', 'search')
    )
def display_page(pathname,search):
    if pathname == '/':
        return home.layout
    # elif pathname == '/Network':
    #     return sbml_network.layout
    elif pathname == '/Contact':
        return contact.layout
    elif pathname == '/Network2':
        return network.layout
    elif pathname == '/Tutorial':
        return tutorial.layout
    elif pathname == '/not-available':
        return not_available.layout(search)

    return html.Div("404: Page not found")


dash_app.clientside_callback(
    *uniprot_and_lipid_redirect_callback(),
    prevent_initial_call=True,
)


dash_app.clientside_callback(
*recenter_cytoscape_graph(),
prevent_initial_call=True
)



from flask import jsonify

@server.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == '__main__':
    dash_app.run(debug=True)
