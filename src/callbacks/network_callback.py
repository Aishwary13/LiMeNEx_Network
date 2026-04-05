import time
from dash import MATCH, html, dcc, callback, Input, Output, State, no_update,ctx
import os
import json
from utils.network_utils import create_nodes_and_edges, processElements, build_dataframe, highlight_elements, remove_highlight, populate_table
import pandas as pd
from itertools import chain
import dash

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
    dropdownOptions = json.load(file)
    databaseCategory = dropdownOptions["databaseCategory"]
    pathway_name_mapping = dropdownOptions["pathway_name_mapping"]
    
with open(os.path.join(root_dir, 'src/sbmlData/metabolite_link_map.json')) as file:
    metabolite_link_map = json.load(file)

################################################### download callbacks###################################################

@callback(
    Output("warning-modal", "is_open"),
    Output("modal-text", "children"),
    Input("Modal-store", "data"),
    State("warning-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(data, is_open):
    if data:
        return not is_open, data

    return False, ""



@callback(
    Output({'type': 'download-target-json', 'index': MATCH}, 'data'),
    Input({'type': 'download-json-btn', 'index': MATCH}, 'n_clicks'),
    State({'type': 'cy-graph', 'index': MATCH}, 'elements'),
    prevent_initial_call=True,
)
def download_graph_json(n_clicks, elements):
    if n_clicks is None or not elements:
        return dash.no_update,"console is Empty"

    payload = json.dumps(elements, indent=2)

    return dcc.send_bytes(
        lambda buffer: buffer.write(payload.encode("utf-8")),
        filename="graph_elements.json"
    )


@callback(
    Output({'type': 'cy-graph', 'index': MATCH}, 'generateImage'),
    Input({'type': 'download-png-btn', 'index': MATCH}, 'n_clicks'),
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
    State({'type': 'info-table', 'index': MATCH}, 'virtualRowData'),
    prevent_initial_call=True
)
def download_table_csv(n_clicks, virtual_data):

    if not virtual_data:
        raise dash.exceptions.PreventUpdate

    df = pd.DataFrame(virtual_data)

    filename = f"table_export_{pd.Timestamp.now():%Y%m%d_%H%M%S}.csv"

    return dcc.send_data_frame(
        df.to_csv,
        filename,
        index=False
    )

############################### edge information ################################################################

def return_erorr_messgae(fetch = False,genes = False,lipid = False):
    
    message = "An Error Occured, Please try again. If the issue persists contact Us."
    message2 = "Please select atleast 1 lipid to continue."
    message3 = "Please select atleast 1 Gene to continue."
    
    if fetch:
        if genes:
            return message3
        else:
            return message2
    return message


@callback(
    Output('Modal-store','data',allow_duplicate=True),
    Output('cytoscape-pop-pre', 'children'),
    Output('cytoscape-tap-edge-data-output', 'style'),
    Input({'type': 'cy-graph','index':'console-2'}, 'tapEdgeData'),
    prevent_initial_call=True
)
def show_popup(tap_edge_data):
    """Show popup with pretty JSON when an edge is tapped."""
    try :
        if not tap_edge_data:
            return no_update, {'display': 'none'}, no_update

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

        return no_update,pretty_text, container_style
    
    except Exception as e:
        return return_erorr_messgae(),no_update,no_update


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


@callback(
    Output({'type': 'cy-graph','index':'console-1'}, 'elements'),
    Output({'type': 'cy-graph','index':'console-1'},'stylesheet'),
    Input("cy-elements-store", "data"),
    State({'type': 'cy-graph','index':'console-1'},'stylesheet'),
    prevent_initial_call=True
)
def render_graph(data,stylesheet):

    if not data:
        return [], dash.no_update

    print("Rendering graph in Cytoscape…")

    # HARD RESET: clear first
    # elements = []

    # # FULL GRAPH: then add everything
    # elements = data["nodes"] + data["edges"]

    return data,stylesheet


def validate_parents(nodes):
    """
    Validates that every node with data.parent refers to an existing node id.
    Returns a list of errors.
    """
    errors = []

    node_ids = {n["data"]["id"] for n in nodes}

    for n in nodes:
        parent = n["data"].get("parent")
        if parent and parent not in node_ids:
            errors.append(
                f"Node '{n['data']['id']}' has missing parent '{parent}'"
            )
    return errors

@callback(
    Output('Modal-store','data',allow_duplicate=True),
    Output("cy-elements-store", "data"),
    Output({'type': 'info-table', 'index': 'console-1'},'rowData'),
    Output({'type': 'info-table', 'index': 'console-1'},'columnDefs'),
    Output('main-chain-lipid-dropdown','options'),
    Output('main-chain-lipid-dropdown','value'),
    Output('highlight-radio','options'),
    Output('current-lipid-store','data'),
    Input('fetch-network-button', 'n_clicks'),
    State('lipid-dropdown', 'value'),
    State('highlight-radio','options'),
    prevent_initial_call=True,
    running=[(Output("fetch-network-button", "disabled"), True, False)]
)
def fetch_network(n_clicks, selected_lipids, highlight_options):
    
    try :
        finalNodes, finalEdges, pathway_info_children = [], [], []
        
        if n_clicks is None or not selected_lipids:
            return return_erorr_messgae(fetch=True,lipid=True),no_update,no_update,no_update,no_update, no_update, no_update, no_update
        
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
        finalNodes, finalEdges, lipids_for_rxn_mode = create_nodes_and_edges(pathways,selected_lipids)
        elements = finalNodes + finalEdges
        
        #output for pathway info container
        pathway_info_children = []
                    
        # build infor cards
        bundled_info = []
        for pathway, lipids in pathway_lipids.items():
            # database_list = ["Kegg","Reactome"]  # Example database list
            database = databaseCategory.get(pathway, "None")
            temp = {}
            temp['Pathway'] = pathway_name_mapping[pathway]
            temp['Databases'] = database
            temp['Lipids'] = lipids
            bundled_info.append(temp)
            # card = return_pathway_card(pathway, lipids, database)
            # pathway_info_children.append(card)
        
        columnDefs = [
            {"field": "Lipids", "flex": 1},
            {"field": "Pathway", "flex": 1},
            {"field": "Databases", "flex": 1},
        ]
        
        
        #########################
        node_ids = {n['data']['id'] for n in finalNodes}
        for e in finalEdges:
            if e['data']['source'] not in node_ids:
                print("❌ Missing source node:", e['data']['source'])
            if e['data']['target'] not in node_ids:
                print("❌ Missing target node:", e['data']['target'])

        
        for n in finalNodes:
            if 'parent' in n['data'] and n['data']['parent'] not in node_ids:
                print("❌ Missing parent:", n['data']['parent'], "for", n['data']['id'])

        
        ##########################
        
        parent_errors = validate_parents(finalNodes)
        if parent_errors:
            print("❌ Parent integrity errors:")
            for e in parent_errors:
                print("  ", e)
        else:
            print("✅ All parent references are valid")
                
        print("Passed all the checks")
        
        
        # set diable to true, enable reaction view
        options = [{**x, "disabled": False} for x in highlight_options]
        option_value = 1 #reset to full network
        rxn_view_lipids = [] #remove all previous selections for reaction view mode
        
        return no_update,elements,bundled_info,columnDefs,lipids_for_rxn_mode,rxn_view_lipids,options,selected_lipids

    except Exception as e:
        print(f"Error in fetch_network: {e}")
        return return_erorr_messgae(),no_update, no_update, no_update,no_update, no_update, no_update, no_update


@callback(
    Output('Modal-store','data',allow_duplicate=True),
    Output({'type': 'cy-graph','index':'console-1'},'elements', allow_duplicate=True),
    Output("main-chain-lipid-dropdown",'disabled'),
    Output('lipid-dropdown','disabled'),
    Output('fetch-network-button','disabled'),
    Input('highlight-radio','value'),
    State({'type': 'cy-graph','index':'console-1'},'elements'),
    State('main-chain-lipid-dropdown','value'),
    prevent_initial_call=True,
)
def highlight_reaction_Chain(value, elements, selected_lipids):
    try:
        if value is None:
            print("Direct pathway toggle value is None")
            return elements, no_update, no_update, no_update, no_update
        
        print("Direct pathway toggle value:", value)
        print(selected_lipids)
        
        to_disable = False # whether to diable the lipid input
        if value == 2:
            elements = highlight_elements(elements, selected_lipids)
            to_disable = True
        else:
            elements = remove_highlight(elements, selected_lipids)
            to_disable = False
        
        return no_update,elements,to_disable, to_disable, to_disable
    except Exception as e:
        return return_erorr_messgae(),no_update, no_update, no_update, no_update



# @callback(
#     Output({'type': 'cy-graph','index':'console-1'},'elements', allow_duplicate=True),
#     Input('main-chain-lipid-dropdown','value'),
#     State({'type': 'cy-graph','index':'console-1'},'elements'),
#     State('current-lipid-store','data'),
#     prevent_initial_call=True,
# )
# def highlight_selected_lipids(lipids,elements, current_lipids):
    
#     if elements is None or lipids is None or not elements:
#         return no_update
    
#     print("-------current_lipids" , current_lipids)
    
#     for ele in elements:
#         if 'source' not in ele['data']:
#             if ele['data']['id'] in current_lipids:
#                 continue
            
#             if ele['data']['id'] in lipids:
#                 var = ele['data']['classes'].split(" ")
#                 if 'highlightedNode' not in var:
#                     ele['data']['classes'] += ' highlightedNode'
#                     ele['classes'] = ele['data']['classes']
#             else:
#                 var = ele['data']['classes'].split(" ")
#                 if 'highlightedNode' in var:
#                     ele['data']['classes'] = " ".join(var[:-1])
#                     ele['classes'] = ele['data']['classes']            
    
#     return elements




@callback(
    Output('Modal-store','data',allow_duplicate=True),
    Output({'type': 'cy-graph','index':'console-3'},'elements'),
    Output({'type': 'cy-graph','index':'console-3'},'stylesheet'),
    Output({'type': 'info-table', 'index': 'console-3'},'rowData'),
    Output({'type': 'info-table', 'index': 'console-3'},'columnDefs'),
    Input('fetch-tfs-button', 'n_clicks'),
    State('gene-dropdown', 'value'),
    State({'type': 'cy-graph','index':'console-3'}, 'stylesheet'),
    prevent_initial_call=True,
    running=[(Output("fetch-tfs-button", "disabled"), True, False)]
)
def fetch_tfs(n_clicks, selected_genes, stylesheet):

    try:
        if n_clicks is None or not selected_genes:
            return return_erorr_messgae(fetch=True,genes=True), no_update, stylesheet, no_update, no_update

        finalNodes = []
        finalEdges = []
        finalTargetGene = set()

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
                edgeTissues = " ".join(tissueList)
                tf_tissueList.update(tissueList)
                global_tissues.update(tissueList)
                
                if not temp.empty:
                    if tg not in finalTargetGene:
                        finalTargetGene.add(tg)
                        finalNodes.append({
                            'data': {'id': tg, 'label': tg, 'classes': 'enzymaticGene','uniprotAcc': uniprot_cache.get(tg,'')},
                            'classes': 'enzymaticGene',
                        })
                    
                    finalEdges.append({
                        'data': {'source': tf, 'target': tg, 'tissueClass' : f"TRANSCRIPTION {edgeTissues}"},
                        'classes' : f"TRANSCRIPTION",
                    })
            
            nodeTissues = " ".join(tf_tissueList)
            finalNodes.append({
                'data': {'id': tf, 'label': tf, 'tissueClass' : f"transcriptionFactorGene {nodeTissues}",'uniprotAcc': uniprot_cache.get(tf,'')},
                'classes': "transcriptionFactorGene",
            })
                    
        elements = finalNodes + finalEdges
        
        # build table data
        # tf, gene = populate_table_dropdown(1,elements)
        tf = list(transcription_factors)
        gene = list(finalTargetGene)
        df, columnDefs = populate_table(tf_value=tf,gene_value=gene)
        
        return no_update, elements, stylesheet, df, columnDefs
    
    except Exception as e:
        return return_erorr_messgae(), no_update, no_update, no_update, no_update


def _changeTissueOptions_core(phySystemOptions):
    try:
        global psToTissue
        # Return placeholder option if no physiological system is selected
        if phySystemOptions is None or len(phySystemOptions) == 0:
            return no_update, [{'label': 'Select Physiological System To View Tissues List', 'value': 'null'}]

        if len(phySystemOptions) != 0:
            # Collect tissues and format labels with the system name
            tissueOptions = []  
            for system in phySystemOptions:
                tissues = psToTissue.get(system, [])
                for tissue in tissues:
                    tissueOptions.append({'label': f"{system}: {tissue}", 'value': tissue})

            return no_update, tissueOptions
        else:
            return no_update, [{'label': 'Select Physiological System To View Tissues List', 'value': 'null'}]
    except Exception as e:
        return return_erorr_messgae(), no_update


# --- helper 2: original handlePhysiologicalSelection logic, unchanged ---
def _handlePhysiologicalSelection_core(val, stylesheet, elements):
    try:
        global tissueToPs
        global psToTissue

        if val is None:
            return no_update, stylesheet, elements

        val = set(val)

        allowedTissues = list(chain(*[psToTissue[sys] for sys in val]))
        allowedTissues = set([var for var in allowedTissues])
        newElements = processElements(elements, allowedTissues)

        return no_update, stylesheet, newElements
            
    except Exception as e:
        return return_erorr_messgae(), no_update, no_update


@callback(
    Output('Modal-store', 'data', allow_duplicate=True),
    Output("tissue-dropdown", "options"),
    Output({'type': 'cy-graph', 'index': 'console-3'}, "stylesheet", allow_duplicate=True),
    Output({'type': 'cy-graph', 'index': 'console-3'}, "elements", allow_duplicate=True),
    Input("physiological-systems-dropdown", "value"),
    State({'type': 'cy-graph', 'index': 'console-3'}, "stylesheet"),
    State({'type': 'cy-graph', 'index': 'console-3'}, "elements"),
    prevent_initial_call=True,
)
def combined_physio_selection(phySystemOptions, stylesheet, elements):
    # run the two original logics independently
    
    modal1, tissue_options = _changeTissueOptions_core(phySystemOptions)
    modal2, new_stylesheet, new_elements = _handlePhysiologicalSelection_core(
        phySystemOptions, stylesheet, elements
    )

    # choose which Modal-store message to show:
    # - if the first produced an error/message, prefer it
    # - otherwise use the second one
    if modal1 is not no_update:
        modal_data = modal1
    else:
        modal_data = modal2

    return modal_data, tissue_options, new_stylesheet, new_elements


@callback(
    Output('Modal-store','data',allow_duplicate=True),
    Output({'type': 'cy-graph','index':'console-3'}, "stylesheet", allow_duplicate=True),
    Output({'type': 'cy-graph','index':'console-3'},"elements",allow_duplicate= True),
    Input("tissue-dropdown", "value"),
    State({'type': 'cy-graph','index':'console-3'}, "stylesheet"),
    State("physiological-systems-dropdown","value"),
    State({'type': 'cy-graph','index':'console-3'},"elements"),
    prevent_initial_call=True,
)
def handleTissueSelection(tisOptions, stylesheet,phySystemOptions,elements):
    try:
        if tisOptions is None:
            return no_update,stylesheet, elements
        
        if len(tisOptions) != 0:

            if 'null' in tisOptions:
                return no_update,stylesheet,no_update

            allowedTissue = set([var for var in tisOptions])

            newElements = processElements(elements,allowedTissue)
        
            return no_update,stylesheet ,newElements
        else:
            return _handlePhysiologicalSelection_core(phySystemOptions,stylesheet, elements)
    except Exception as e:
        return return_erorr_messgae(), no_update, no_update


@callback(
    Output('Modal-store','data',allow_duplicate=True),
    Output({'type': 'info-table', 'index': 'console-2'}, "rowData"),
    Output({'type': 'info-table', 'index': 'console-2'}, "columnDefs"),
    Output({'type': 'cy-graph','index':'console-2'},'elements'),
    Output({'type': 'cy-graph','index':'console-2'},'stylesheet'),
    Input('fetch-reactions-button', 'n_clicks'),
    State('gene-rxn-dropdown', 'value'),
    State({'type': 'cy-graph','index':'console-2'},'stylesheet'),
    prevent_initial_call = True,
    running=[(Output("fetch-reactions-button", "disabled"), True, False)]
)
def fetch_rxn(n_clicks, genes, stylesheet):
    try:
        if not n_clicks or not genes:
            return return_erorr_messgae(fetch=True,genes=True),[],[],no_update
        
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
                    pathway.update(set(finalReactionList[key]['pathways']))
                    finalReactionList[key]['pathways'] = list(pathway)
                    continue
                
                finalReactionList[key] = value.get('pathways',[])
                finalReactionList[key] = {'pathways' : value.get('pathways',[]), 'value' : value}
                
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
                            'data': {'id': reactant, 'label':reactant,'classes' : 'lipidMetabolite', 'link': metabolite_link_map.get(reactant,'')},
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
                            'data': {'id': product, 'label':product,'classes' : 'lipidMetabolite', 'link': metabolite_link_map.get(product,'')},
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
        
        # print(finalReactionList)
        
        df, columnDefs = build_dataframe(finalReactionList)
        
        finalNodes.extend(finalLipidNodes.values())
        
        return no_update, df.to_dict('records'), columnDefs,finalNodes+finalEdges , stylesheet
    except Exception as e:
        return return_erorr_messgae(), no_update, no_update, no_update
    
