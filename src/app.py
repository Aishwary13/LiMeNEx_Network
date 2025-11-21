import dash
from dash import html,dcc,MATCH,ALL
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import dash_cytoscape as cyto
import diskcache
from dash import DiskcacheManager
import os
import pandas as pd

font_awesome1 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css'
font_awesome3 = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/solid.min.css'

external_js_lib="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
local_warn_suppressor = "/assets/ignore_wheel_warn.js"

os.environ['TMPDIR'] = 'C:\\Temp'

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheManager(cache)

dash_app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,font_awesome1,font_awesome3],
                    title="LiMeNex" ,use_pages=True,suppress_callback_exceptions=True,
                    external_scripts=[external_js_lib, local_warn_suppressor],background_callback_manager=long_callback_manager)

cyto.load_extra_layouts()

from pages import home, contact,sbml_network,network
from callbacks import network_callback

dataBasePath= sbml_network.dataBasePath

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
                    html.Img(src="assets/Title.png", style={"width": "9rem"})
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
                    className="pe-3",
                ),
                dbc.NavLink([html.Div([
                    html.I(className="fa-solid fa-circle-nodes"),
                    html.Span("Network-2", style={'marginTop': '0px', 'marginLeft' :'6px'})], className='icon_title')],
                    href="/Network2",
                    active="exact",
                    className="pe-3",
                    style={'marginTop' : '7px'}
                ),
                dbc.NavLink([html.Div([
                    html.I(className="fa-solid fa-circle-nodes"),
                    html.Span("Network", style={'marginTop': '0px', 'marginLeft' :'6px'})], className='icon_title')],
                    href="/Network",
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
                )
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
    )
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/Network':
        return sbml_network.layout
    elif pathname == '/Contact':
        return contact.layout
    elif pathname == '/Network2':
        return network.layout


@dash_app.callback(
    Output('cytoscape', 'elements',allow_duplicate=True),
    Output('cytoscape','stylesheet', allow_duplicate=True),
    Output('followers-node-store','data'),
    Output('followers-edge-store','data'),
    Output('dataframe-store','data'),
    Input('fetchPathwaysButton','n_clicks'),
    State('pathwayDropdownOptions', 'value'),
    State('cytoscape','stylesheet'),
    running=[
        (
            Output("progress-container", "style"),
            {"display": "block","value" : '0','max' : '10',"position":"fixed","top":"0","left":"0","zIndex" : '1002', "width": "100vw", "height": "100vh",  "background": "rgba(0, 0, 0, 0.5)", "backdrop-filter": "blur(5px)"},
            {"display": "none"},
        )
    ],
    progress=[Output("progress-bar", "value"), Output("progress-bar", "max")],
    prevent_initial_call = True,
    background=True
)
def handlePathwaySelection(set_progress,n_clicks,optionList,stylesheet):
    if optionList is None:
        return [], stylesheet,{},{},{}

    if len(optionList) != 0:
        set_progress(('0','10'))

        followers_edges_di = {}
        followers_node_di = {}

        finalNodes = []
        finalEdges = []
        finalNodeSet = set()
        finalReactionList = []
        reactionNum = 1

        total_files = len(optionList)
        try:
            inc = 10/total_files
        except:
            set_progress(('10','10'))
        # init = 0

        dfList = []
        for i,fileName in enumerate(optionList):
            # filePathSbml = os.path.join(dataBasePath,'networkFile',f"{fileName}.xml")
            filePathTf = os.path.join(dataBasePath,'pathwayTfsModified',f"{fileName}.csv")
            reactionNum = sbml_network.readSbml(fileName=fileName,finalNodes=finalNodes,finalNodeSet=finalNodeSet,finalEdges=finalEdges, reactionNum=reactionNum)
            
            if os.path.exists(filePathTf):
                temp = pd.read_csv(filePathTf)
                dfList.append(temp)

        df = pd.DataFrame()

        if len(dfList) != 0:
            df = pd.concat(dfList, ignore_index=True)

            # adding display stylesheet for each tissue
            uniqueTissue = df['Tissue'].unique()
            for tis in uniqueTissue:
                stylesheet.extend([{
                    "selector" : f".{tis}_T",
                    "style" : {"display" : "element"}
                }])
            
            for progress in sbml_network.readMapping(df=df,finalNodes=finalNodes,finalEdges=finalEdges, finalNodeSet=finalNodeSet,followers_node_di=followers_node_di,followers_edges_di=followers_edges_di):
                set_progress((progress,'10'))

        # print(followers_edges_di)
        dataframe_json = df.to_json(orient='split')
        return finalNodes+finalEdges, stylesheet,followers_node_di,followers_edges_di,dataframe_json
    else:
        new_stylesheet = []
        for style in stylesheet:
            if 'T_' != style.get('selector')[-1:-3:-1]:
                new_stylesheet.append(style)

        return [], new_stylesheet,{},{},{}


# correct clientside callback registration (paste into Python)
# dash_app.clientside_callback(
#     """
#     async function(n_clicks) {
#         // If no clicks, do nothing (prevent_initial_call will usually avoid this)
#         // But return no_update if you want to be extra safe:
#         if (typeof n_clicks === 'undefined' || n_clicks === null) {
#             return window.dash_clientside.no_update;
#         }

#         // children (empty string) and style object
#         const children = "";
#         const style = {
#             display: "none",
#             position: "absolute",
#             top: "15px",
#             right: "15px",
#             zIndex: 2000
#         };

#         // MUST return an array matching the Outputs order
#         return [children, style];
#     }
#     """,
#     Output("cytoscape-pop-pre", "children", allow_duplicate=True),
#     Output("cytoscape-tap-edge-data-output", "style", allow_duplicate=True),
#     Input("cytoscape-pop-close-btn", "n_clicks"),
#     prevent_initial_call=True,
# )


dash_app.clientside_callback(
    """
    function(data1,data2,data3) {
        const data = data1 || data2 || data3;
        
        // console.log("Tapped node data:", data);
        
        if (!data || !('uniprotAcc' in data) || data.uniprotAcc.length === 0) {
            return window.dash_clientside.no_update;
        }
        window.open(`https://www.uniprot.org/uniprotkb/${data.uniprotAcc}`, "_blank");
        
        delete data1;
        delete data2;
        delete data3;
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-output-store", "data"),
    Input({'type': 'cy-graph','index':'console-1'}, "tapNodeData"),
    Input({'type': 'cy-graph','index':'console-2'}, "tapNodeData"),
    Input({'type': 'cy-graph','index':'console-3'}, "tapNodeData"),
    prevent_initial_call=True,
)


if __name__ == '__main__':
    dash_app.run(debug=True)
