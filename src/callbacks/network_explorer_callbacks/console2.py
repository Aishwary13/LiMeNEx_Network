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

from utils.network_utils import build_dataframe

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


def return_erorr_messgae3(fetch = False,genes = False,lipid = False):
    
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
        return return_erorr_messgae3(),no_update,no_update


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
            return return_erorr_messgae3(fetch=True,genes=True),[],[],no_update
        
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
        return return_erorr_messgae3(), no_update, no_update, no_update