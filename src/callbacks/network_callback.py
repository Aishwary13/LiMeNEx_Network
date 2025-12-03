import time
from dash import MATCH, html, dcc, callback, Input, Output, State, no_update
import os
import json
from utils.network_utils import create_nodes_and_edges, processElements, build_dataframe, highlight_elements, remove_highlight
import pandas as pd
from itertools import chain
import dash
import dash_cytoscape as cyto

from dotenv import load_dotenv

load_dotenv()
root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")
with open(os.path.join(root_dir, 'src/sbmlData/lipid_pathway_map.json')) as file:
    lipid_map = json.load(file)

with open(os.path.join(root_dir, 'src/sbmlData/psToTissue.json')) as file:
    psToTissue = json.load(file)

with open(os.path.join(root_dir, 'src/sbmlData/tissueToPs.json')) as file:
    tissueToPs = json.load(file)
    
with open(os.path.join(root_dir, 'src/sbmlData/uniprot_cache.json')) as file:
    uniprot_cache = json.load(file)
    

with open(os.path.join(root_dir,'src/sbmlData/pathwayDropdownOptions.json'), 'r') as file:
    # Load the JSON data
    dropdownOptions = json.load(file)
    # pathwayDropdownOptions = dropdownOptions["PathwayOptions"]
    # physiologicalSystemOptions = dropdownOptions["physiologicalOptions"]
    databaseCategory = dropdownOptions["databaseCategory"]

################################################### download callbacks###################################################

@callback(
    Output({'type': 'download-target-json', 'index': MATCH}, 'data'),
    Input({'type': 'download-json-btn', 'index': MATCH}, 'n_clicks'),
    State({'type': 'cy-elements-store', 'index': MATCH}, 'data'),
    prevent_initial_call=True,
)
def download_graph_json(n_clicks, elements):
    if not elements:
        elements = []

    payload = json.dumps(elements, indent=2)

    return dcc.send_bytes(
        lambda buffer: buffer.write(payload.encode("utf-8")),
        filename="graph_elements.json"
    )


@callback(
    Output({'type': 'cy-elements-store','index': MATCH}, 'data'),
    Input({'type': 'cy-graph','index': MATCH},'elements'),
    prevent_initial_call=False
)
def mirror_elements_to_store(elements):
    # called whenever elements change; elements may be []
    return elements



from dash import callback, Input, Output, State, MATCH, ctx
import dash

@callback(
    Output({'type': 'cy-graph', 'index': MATCH}, 'generateImage'),
    Input({'type': 'download-png-btn', 'index': MATCH}, 'n_clicks'),
    # optional: read layout/size if you want to dynamically set width/height,
    State({'type': 'cy-graph', 'index': MATCH}, 'layout'),
    prevent_initial_call=True,
)
def trigger_image_export(png_clicks, layout):
    """
    This sets generateImage on the cytoscape with the desired format and action.
    For png/jpg we use action='download' (or 'store' if you want imageData populated).
    For svg we use action='download' (SVG is usually downloaded directly).
    """
    # Determine which button triggered this callback
    triggered = ctx.triggered_id  # pattern id object or None
    if not triggered:
        raise dash.exceptions.PreventUpdate

    ftype = 'svg'
    action = 'download' 

    # Optionally compute width/height based on layout or other state
    # e.g. width=1600, height=1200 for high-res png
    image_opts = {
        'type': ftype,
        'action': action
    }

    # If you want specific size for raster formats:
    # if ftype in ('png','jpg'):
    #     image_opts.update({'scale': 2, 'background': 'white', 'width': 1600, 'height': 1200})

    return image_opts


@callback(
    Output({'type': 'download-target-csv', 'index': MATCH}, 'data'),
    Input({'type': 'download-csv-btn', 'index': MATCH}, 'n_clicks'),
    State({'type': 'info-table', 'index': MATCH}, 'derived_virtual_data'),
    prevent_initial_call=True
)
def download_table_csv(n_clicks, derived_data):
    if not derived_data:
        raise dash.exceptions.PreventUpdate

    df = pd.DataFrame(derived_data)
    # optional: sanitize/format df here

    filename = f"table_export_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv"
    return dcc.send_data_frame(df.to_csv, filename, index=False)

############################### edge information ################################################################

@callback(
    Output('cytoscape-pop-pre', 'children'),
    Output('cytoscape-tap-edge-data-output', 'style'),
    Input({'type': 'cy-graph','index':'console-2'}, 'tapEdgeData'),
    prevent_initial_call=True
)
def show_popup(tap_edge_data):
    """Show popup with pretty JSON when an edge is tapped."""
    if not tap_edge_data:
        return "", {'display': 'none'}

    reactInfo = tap_edge_data.get('reactInfo', 'No reaction info available.')

    info = {'Reaction Info': reactInfo}
    pretty_text = json.dumps(info, indent=2)

    # parent style: make visible and run slideIn animation (forwards to remain)
    container_style = {
        'display': 'block',
        'animation': 'slideIn 250ms ease forwards',
        '-webkit-animation': 'slideIn 250ms ease forwards',
        'position': 'absolute',
        'top': '15px',
        'right': '15px',
        'zIndex': 2000
    }

    return pretty_text, container_style



@callback(
    Output('cytoscape-pop-pre', 'children',allow_duplicate=True),
    Output('cytoscape-tap-edge-data-output', 'style',allow_duplicate=True),
    Input('cytoscape-pop-close-btn', 'n_clicks'),
    prevent_initial_call=True
)
def close_popup(n_clicks):
    """Hide and clear the popup when close button is clicked."""
    # return empty children and hide container
    hidden_style = {
        'display': 'none',
        'position': 'absolute',
        'top': '15px',
        'right': '15px',
        'zIndex': 2000
    }
    return "", hidden_style


####################################################################################################################

def return_pathway_card(pathways, lipid_list, database):
    
    return html.Div(
        [
            html.Div("Pathway:", className="pinfo-label"),
            html.Div(pathways, className="pinfo-value"),

            html.Div("Lipids:", className="pinfo-label"),
            html.Div(", ".join(lipid_list), className="pinfo-value"),

            html.Div("Database:", className="pinfo-label"),
            html.Div(database, className="pinfo-value"),
        ],
        className="pinfo-card"
    )
    


@callback(
    Output({'type': 'cy-graph','index':'console-1'},'elements'),
    Output({'type': 'cy-graph','index':'console-1'},'stylesheet'),
    Output('pathway-info-container','children'),
    Input('fetch-network-button', 'n_clicks'),
    State('lipid-dropdown', 'value'),
    State({'type': 'cy-graph','index':'console-1'},'stylesheet'),
    prevent_initial_call=True,
    running=[(Output("fetch-network-button", "disabled"), True, False)]
    # background=True
)
def fetch_network(n_clicks, selected_lipids,stylesheet):
    
    try :
        
        finalNodes, finalEdges, pathway_info_children = [], [], []
        
        if n_clicks is None or not selected_lipids:
            return [],stylesheet,dash.no_update # No clicks or no lipids selected, return empty list
        
        print(f"Selected lipids: {selected_lipids}")
        #get all pathways for selected lipids
        pathway_lipids = {}
        pathways = set()
        for lipid in selected_lipids:
            if lipid in lipid_map:
                pathways.update(lipid_map[lipid])
                
                for pathway in lipid_map[lipid]:
                    if pathway not in pathway_lipids:
                        pathway_lipids[pathway] = []
                    pathway_lipids[pathway].append(lipid)
            else:
                print(f"Lipid {lipid} not found in lipid_map")

        #create nodes and edges
        finalNodes, finalEdges = create_nodes_and_edges(pathways,selected_lipids)
        elements = finalNodes + finalEdges
        
        #output for pathway info container
        pathway_info_children = []
                    
        # build infor cards
        for pathway, lipids in pathway_lipids.items():
            # database_list = ["Kegg","Reactome"]  # Example database list
            database = databaseCategory.get(pathway, "None")
            card = return_pathway_card(pathway, lipids, database)
            pathway_info_children.append(card)
        

        return elements,stylesheet,pathway_info_children

    except Exception as e:
        print(f"Error in fetch_network: {e}")
        return [], stylesheet, dash.no_update


@callback(
    Output({'type': 'cy-graph','index':'console-1'},'elements', allow_duplicate=True),
    Input('direct-pathway-toggle','value'),
    State({'type': 'cy-graph','index':'console-1'},'elements'),
    State('lipid-dropdown','value'),
    prevent_initial_call=True,
)
def highlight_reaction_Chain(value, elements, selected_lipids):

    if value is None:
        print("Direct pathway toggle value is None")
        return elements
    
    print("Direct pathway toggle value:", value)
    
    if 'highlight' in value:
        elements = highlight_elements(elements, selected_lipids)
    else:
        elements = remove_highlight(elements, selected_lipids)
    
    return elements


@callback(
    Output({'type': 'cy-graph','index':'console-3'},'elements'),
    Output({'type': 'cy-graph','index':'console-3'},'stylesheet'),
    Output("graph-update-flag", "data"),
    Input('fetch-tfs-button', 'n_clicks'),
    State('gene-dropdown', 'value'),
    State({'type': 'cy-graph','index':'console-3'}, 'stylesheet'),
    prevent_initial_call=True,
    running=[(Output("fetch-tfs-button", "disabled"), True, False)]
)
def fetch_tfs(n_clicks, selected_genes, stylesheet):

    if n_clicks is None or not selected_genes:
        return [], stylesheet, {"updated": False}

    # Here you would implement the logic to fetch the transcription factors
    # based on the selected genes and the current elements of the pathway-gene-graph.

    # For demonstration purposes, let's assume we found some TFs.
    finalNodes = []
    finalEdges = []
    finalNodeSet = set()

    df = pd.read_csv(os.path.join(root_dir, 'src/sbmlData/final_tf_targetgene_tissue_groups.csv'), dtype=str)
    transcription_factors = df[df['TargetGene'].isin(selected_genes)]['TF'].unique().tolist()
    global_tissues = set()
    for tf in transcription_factors:
        # mask2 = df['TF'] == tf
        # temp2 = df[mask2]
        # tissueList = temp2['Tissue'].unique().tolist()
        # nodeTissues = "_T".join(tissueList) + "_T"
        tf_tissueList = set()
        
        for tg in selected_genes:
            mask = (df['TF'] == tf) & (df['TargetGene'] == tg)
            temp = df[mask]
            tissueList = temp['Tissue'].unique().tolist()
            edgeTissues = "_T ".join(tissueList) + "_T"
            tf_tissueList.update(tissueList)
            global_tissues.update(tissueList)
            
            if not temp.empty:
                if tg not in finalNodeSet:
                    finalNodeSet.add(tg)
                    finalNodes.append({
                        'data': {'id': tg, 'label': tg, 'classes': 'enzymaticGene','uniprotAcc': uniprot_cache.get(tg,'')},
                        'classes': 'enzymaticGene',
                    })
                
                finalEdges.append({
                    'data': {'source': tf, 'target': tg, 'tissueClass' : f"TRANSCRIPTION {edgeTissues}"},
                    'classes' : f"TRANSCRIPTION",
                })
        
        nodeTissues = "_T ".join(tf_tissueList) + "_T"
        finalNodes.append({
            'data': {'id': tf, 'label': tf, 'tissueClass' : f"transcriptionFactorGene {nodeTissues}",'uniprotAcc': uniprot_cache.get(tf,'')},
            'classes': "transcriptionFactorGene",
        })
    
    
    # uniqueTissue = tissueToPs.keys()
    for tis in global_tissues:
        stylesheet.extend([{
            "selector" : f".{tis}_T",
            "style" : {"display" : "element"}
        }])
        # Add a corresponding edge for the tissue
    
    elements = finalNodes + finalEdges
    return elements, stylesheet, {"updated": True}


@callback(
    Output("tissue-dropdown", "options"),
    Input("physiological-systems-dropdown", "value"),
)
def changeTissueOptions(phySystemOptions):
    global psToTissue
    # Return placeholder option if no physiological system is selected
    if phySystemOptions is None or len(phySystemOptions) == 0:
        return [{'label': 'Select Physiological System To View Tissues List', 'value': 'null'}]

    if len(phySystemOptions) != 0:
        # Collect tissues and format labels with the system name
        tissueOptions = []  
        for system in phySystemOptions:
            tissues = psToTissue.get(system, [])
            for tissue in tissues:
                tissueOptions.append({'label': f"{system}: {tissue}", 'value': tissue})

        return tissueOptions
    else:
        
        return [{'label': 'Select Physiological System To View Tissues List', 'value': 'null'}]



@callback(
    Output({'type': 'cy-graph','index':'console-3'}, "stylesheet", allow_duplicate= True),
    Output({'type': 'cy-graph','index':'console-3'},"elements",allow_duplicate= True),
    Input("physiological-systems-dropdown", "value"),
    State({'type': 'cy-graph','index':'console-3'}, "stylesheet"),
    State({'type': 'cy-graph','index':'console-3'},"elements"),
    prevent_initial_call=True,
)
def handlePhysiologicalSelection(val,stylesheet, elements):
    global tissueToPs
    global psToTissue

    if val is None:
        return stylesheet,elements

    if len(val) != 0:
        val = set(val)
        basic_stylesheet = []
        show_stylesheet = []
        hide_stylesheet = []

        for style in stylesheet:
            selector = style.get('selector')
            
            if 'T_' == selector[-1:-3:-1]:
                phySystem = set(tissueToPs[(selector[1:-2])])
                if phySystem.intersection(val):
                    style.get('style')['display'] = 'element'
                    show_stylesheet.append(style)
                else:
                    style.get('style')['display'] = 'none'
                    hide_stylesheet.append(style)
            else:
                basic_stylesheet.append(style)
        
        
        basic_stylesheet.extend(show_stylesheet)
        basic_stylesheet.extend(hide_stylesheet)

        # print(json.dumps(basic_stylesheet,indent=2))

        allowedTissues = list(chain(*[psToTissue[sys] for sys in val]))
        allowedTissues = set([var+"_T" for var in allowedTissues])
        newElements = processElements(elements,allowedTissues)

        return basic_stylesheet, newElements

    else:
        for style in stylesheet:
            if 'T_' == style.get('selector')[-1:-3:-1]:
                style.get('style')['display'] = 'element'

        return stylesheet, elements
    

@callback(
    Output({'type': 'cy-graph','index':'console-3'}, "stylesheet", allow_duplicate=True),
    Output({'type': 'cy-graph','index':'console-3'},"elements",allow_duplicate= True),
    Input("tissue-dropdown", "value"),
    State({'type': 'cy-graph','index':'console-3'}, "stylesheet"),
    State("physiological-systems-dropdown","value"),
    State({'type': 'cy-graph','index':'console-3'},"elements"),
    prevent_initial_call=True,
)
def handleTissueSelection(tisOptions, stylesheet,phySystemOptions,elements):

    if tisOptions is None:
        return stylesheet, elements
    
    if len(tisOptions) != 0:

        if 'null' in tisOptions:
            return stylesheet

        basic_stylesheet = []
        show_stylesheet = []
        hide_stylesheet = []
        for style in stylesheet:
            selector = style.get('selector')

            if 'T_' == selector[-1:-3:-1]:
                # print(physiologicalSystemDf[(physiologicalSystemDf['Tissue'] == selector[:-2][1:])]['Physiological System'])
                if selector[:-2][1:] in tisOptions:
                    style.get('style')['display'] = 'element'
                    show_stylesheet.append(style)
                else:
                    style.get('style')['display'] = 'none'
                    hide_stylesheet.append(style)
            else:
                basic_stylesheet.append(style)
        
        basic_stylesheet.extend(hide_stylesheet)
        basic_stylesheet.extend(show_stylesheet)

        allowedTissue = set([var+'_T' for var in tisOptions])

        newElements = processElements(elements,allowedTissue)
    
        return basic_stylesheet ,newElements
    else:
        return handlePhysiologicalSelection(phySystemOptions,stylesheet, elements)

    
@callback(
    Output("tf-select", "options"),
    Output("gene-select", "options"),
    Input("graph-update-flag", "data"),
    State({'type': 'cy-graph','index':'console-3'},"elements"),
    prevent_initial_call=True,
)
def populate_table_dropdown(flag, elements):
    
    if flag is None or not flag.get("updated", False):
        return [], []
    
    tf_options = []
    gene_options = []

    for element in elements:
        if "label" in element['data']:
            if 'classes' not in element['data']:
                tf_options.append({'label': element['data']['label'], 'value': element['data']['id']})
            else:
                gene_options.append({'label': element['data']['label'], 'value': element['data']['id']})

    return tf_options, gene_options



@callback(
    Output({'type': 'info-table', 'index': 'console-3'}, 'data'),
    Input('load-evidence-btn', 'n_clicks'),
    State('tf-select', 'value'),
    State('gene-select', 'value'),
    prevent_initial_call=True,
    running=[(Output("load-evidence-btn", "disabled"), True, False)]
)
def populate_table(n_clicks, tf_value, gene_value):
    if not n_clicks or not tf_value or not gene_value:
        return no_update

    # ---- Read CSV ----
    file_path = os.path.join(root_dir, 'src', 'sbmlData', 'final_tf_targetgene_tissue_groups.csv')
    df = pd.read_csv(file_path, dtype=str).fillna("")

    # ---- Filter by TF(s) and Gene(s) ----
    filtered_df = df[
        (df['TF'].isin(tf_value)) &
        (df['TargetGene'].isin(gene_value))
    ]

    # ---- Optional: clean/trim whitespace ----
    # Ensure filtered_df is a DataFrame before calling applymap (Series would raise the "Series is not callable" type error)
    if isinstance(filtered_df, pd.Series):
        # convert Series to single-row DataFrame so applymap works uniformly
        filtered_df = filtered_df.to_frame().T

    filtered_df = filtered_df.map(lambda x: x.strip() if isinstance(x, str) else x) # type: ignore

    # ---- Return for Dash DataTable ----
    return filtered_df.to_dict('records')


@callback(
    Output({'type': 'info-table', 'index': 'console-2'}, 'data'),
    Output({'type': 'cy-graph','index':'console-2'},'elements'),
    Output({'type': 'cy-graph','index':'console-2'},'stylesheet'),
    Input('fetch-reactions-button', 'n_clicks'),
    State('gene-rxn-dropdown', 'value'),
    State({'type': 'cy-graph','index':'console-2'},'stylesheet'),
    prevent_initial_call = True,
    running=[(Output("fetch-reactions-button", "disabled"), True, False)]
)
def fetch_rxn(n_clicks, genes, stylesheet):
    
    if not n_clicks and not genes:
        return [],[]
    
    with open(os.path.join(root_dir, 'src/sbmlData/gene_to_reactions_map.json')) as file:
        gene_to_rxn = json.load(file)

    finalNodes = []
    finalEdges = []
    finalNodeSet = set()
    finalReactionList = {}
    finalLipidNodes = {}

    for gene in genes:
        rxn = gene_to_rxn.get(gene,{})
        
        for key,value in rxn.items():
            if key in finalReactionList:
                print(f"Reaction {key} already processed, skipping.")
                pathway = set(value.get('pathways',[]))
                pathway.update(set(finalReactionList[key]))
                finalReactionList[key] = list(pathway)
                continue
            
            finalReactionList[key] = value.get('pathways',[])
            
            #create the connector node for reaction
            finalNodes.append({
                'data': {'id': key, 'label':key,'classes' : 'temp'},
                'classes': 'temp',
                # 'selectable': True,
                # 'grabbable': True
            })
            
            
            #create node and edges for reaction
            for reactant in value.get('reactantList',[]):
                if reactant not in finalLipidNodes:
                    finalLipidNodes[reactant] = {
                        'data': {'id': reactant, 'label':reactant,'classes' : 'lipidMetabolite'},
                        'classes': 'lipidMetabolite',
                    }

                
                finalEdges.append({
                    'data': {'source': reactant, 'target': key, 'classes' : 'first_half','reactInfo' : value.get('reactInfo','')},
                    'classes': 'first_half',
                    # 'selectable': True, 
                    # 'grabbable': False
                })
                
            
            for product in value.get('productList',[]):
                if product not in finalLipidNodes:
                    finalLipidNodes[product] = {
                        'data': {'id': product, 'label':product,'classes' : 'lipidMetabolite'},
                        'classes': 'lipidMetabolite',
                        # 'selectable': True,
                        # 'grabbable': True
                    }
                
                finalEdges.append({
                    'data': {'source': key, 'target': product, 'classes' : 'second_half','reactInfo' : value.get('reactInfo','')},
                    'classes': 'second_half',
                    # 'selectable': True, 
                    # 'grabbable': False
                })            


            for gene, modifier in zip(value.get('geneList',[]),value.get('geneModifierType',[])):
                if gene not in finalNodeSet:
                    finalNodeSet.add(gene)
                
                geneNode = {
                    'data': {'id': gene, 'label':gene,'classes' : 'enzymaticGene', 'uniprotAcc': uniprot_cache.get(gene,'')},
                    'classes': 'enzymaticGene',
                    # 'selectable': True,
                    # 'grabbable': True
                }
                
                if gene in genes:
                    geneNode['classes'] += ' highlightedNode'
                
                finalNodes.append(geneNode)
                
                finalEdges.append({
                    'data': {'source': gene, 'target': key, 'classes' : modifier,'reactInfo' : value.get('reactInfo','')},
                    'classes': modifier,
                    # 'selectable': True, 
                    # 'grabbable': False
                })
    
    print(finalReactionList)
    
    df = build_dataframe(finalReactionList)
    
    finalNodes.extend(finalLipidNodes.values())
    
    return df.to_dict('records'), finalNodes+finalEdges , stylesheet
