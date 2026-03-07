from dash import callback, Input, Output, State, no_update
import os
import json
import pandas as pd
from itertools import chain
import sys

file_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if file_path not in sys.path:
    sys.path.insert(0, file_path)

from utils.network_utils import processElements, populate_table

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


def return_erorr_messgae2(fetch = False,genes = False,lipid = False):
    
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
            return return_erorr_messgae2(fetch=True,genes=True), no_update, stylesheet, no_update, no_update

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
                edgeTissues = "_T ".join(tissueList) + "_T"
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
        
        
        # build table data
        # tf, gene = populate_table_dropdown(1,elements)
        tf = list(transcription_factors)
        gene = list(finalTargetGene)
        df, columnDefs = populate_table(tf_value=tf,gene_value=gene)
        
        return no_update, elements, stylesheet, df, columnDefs
    
    except Exception as e:
        return return_erorr_messgae2(), no_update, no_update, no_update, no_update


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
        return return_erorr_messgae2(), no_update


# --- helper 2: original handlePhysiologicalSelection logic, unchanged ---
def _handlePhysiologicalSelection_core(val, stylesheet, elements):
    try:
        global tissueToPs
        global psToTissue

        if val is None:
            return no_update, stylesheet, elements

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
            newElements = processElements(elements, allowedTissues)

            return no_update, basic_stylesheet, newElements

        else:
            for style in stylesheet:
                if 'T_' == style.get('selector')[-1:-3:-1]:
                    style.get('style')['display'] = 'element'

            return no_update, stylesheet, elements
        
    except Exception as e:
        return return_erorr_messgae2(), no_update, no_update


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
        
            return no_update,basic_stylesheet ,newElements
        else:
            return _handlePhysiologicalSelection_core(phySystemOptions,stylesheet, elements)
    except Exception as e:
        return return_erorr_messgae2(), no_update, no_update