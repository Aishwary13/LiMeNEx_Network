import time
from dash import MATCH, dcc, callback, Input, Output, State, no_update,ctx
import os
import json
import pandas as pd
from itertools import chain
import dash
import sys

file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if file_path not in sys.path:
    sys.path.insert(0, file_path)

from utils.network_utils import create_nodes_and_edges, highlight_elements, remove_highlight

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
    
with open(os.path.join(root_dir, 'src/sbmlData/metabolite_link_map.json')) as file:
    metabolite_link_map = json.load(file)


###############################################################################################


def return_erorr_messgae1(fetch = False,genes = False,lipid = False):
    
    message = "An Error Occured, Please try again. If the issue persists contact Us."
    message2 = "Please select atleast 1 lipid to continue."
    message3 = "Please select atleast 1 Gene to continue."
    
    if fetch:
        if genes:
            return message3
        else:
            return message2
    return message


######################################################################################################

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

    # 🔴 HARD RESET: clear first
    # elements = []

    # # 🟢 FULL GRAPH: then add everything
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
            return return_erorr_messgae1(fetch=True,lipid=True),no_update,no_update,no_update,no_update, no_update, no_update, no_update
        
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
            temp['Pathway'] = pathway
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
        return return_erorr_messgae1(),no_update, no_update, no_update,no_update, no_update, no_update, no_update


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
        return return_erorr_messgae1(),no_update, no_update, no_update, no_update