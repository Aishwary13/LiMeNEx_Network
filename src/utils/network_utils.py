import os
import json
from functools import lru_cache
import networkx as nx
from dotenv import load_dotenv
import copy
import pandas as pd

load_dotenv()

root_dir = os.getenv("root_dir_path", default="D:/Raylab/LiMeNEx_Network/")


def load_pathway_data(pathway):
    pathway_file = os.path.join(root_dir, 'src/sbmlData/pathwayInfo', f'{pathway}.json')
    with open(pathway_file, 'r') as f:
        pathway_data = json.load(f)
    return pathway_data

with open(os.path.join(root_dir, 'src/sbmlData/uniprot_cache.json')) as file:
        uniprot_cache = json.load(file)
    
with open(os.path.join(root_dir, 'src/sbmlData/metabolite_link_map.json')) as file:
    metabolite_link_map = json.load(file)


def create_nodes_and_edges(pathways,selected_lipids):
    print("Creating nodes and edges...")
    print("Pathways: ", pathways)

    finalReactionList = set()
    currNodes = {}
    finalEdges = []
    
    finalGeneSet = set()
    genecount = {} 
    
    reaction_gene_nodes = {}
    
      
    # with open(os.path.join(root_dir, 'src/sbmlData/uniprot_cache.json')) as file:
    #     uniprot_cache = json.load(file)
    
    # with open(os.path.join(root_dir, 'src/sbmlData/metabolite_link_map.json')) as file:
    #     metabolite_link_map = json.load(file)
        
    for pathway in pathways:

        pathway_data = load_pathway_data(pathway)
        
        nodes = pathway_data.get('nodes', [])
        reactions = pathway_data.get('reactions', [])
        for key,value in reactions.items():
            
            if key in finalReactionList:
                print(f"Reaction {key} already processed, only updating the parent pathway.")
                if pathway not in currNodes[key]['data']['parent']:
                    currNodes[key]['data']['parent'].append(pathway)
                    
                for gene_node_id in reaction_gene_nodes.get(key, []):
                    if pathway not in currNodes[gene_node_id]['data']['parent']:
                        currNodes[gene_node_id]['data']['parent'].append(pathway)
                            # continue            
            
            #create the connector node for reaction
            if key not in finalReactionList:
                currNodes[key] = {
                    'data': {'id': key, 'label':key,'classes' : 'temp','parent': [pathway]},
                    'classes': 'temp',
                }
            
            intersection = set(selected_lipids).intersection(value.get('reactantList',[]) + value.get('productList',[]))
            if intersection:
                is_selected_lipid_in_reaction = True
            else:
                is_selected_lipid_in_reaction = False
            
            #create node and edges for reaction
            for reactant in value.get('reactantList',[]):
                if reactant not in currNodes:
                    currNodes[reactant] = {
                        'data': {'id': reactant, 'label':reactant,'classes' : nodes.get(reactant,{}).get('class', ''),'parent': [pathway],'link': metabolite_link_map.get(reactant,'')},
                        'classes': nodes.get(reactant,{}).get('class', ''),
                    }
                    
                    if reactant in selected_lipids:
                        currNodes[reactant]['data']['classes'] += ' highlightedNode'
                        currNodes[reactant]['classes'] += ' highlightedNode'
                else:
                    if pathway not in currNodes[reactant]['data']['parent']:
                        currNodes[reactant]['data']['parent'].append(pathway)
                
                if key not in finalReactionList:
                    edge = {
                        'data': {'source': reactant, 'target': key, 'classes' : 'first_half','reactInfo' : value.get('reactInfo',''),'reactionType' : value.get('reactionType','')},
                        'classes': 'first_half',
                    }
                    if is_selected_lipid_in_reaction:
                        edge['classes'] += ' highlightedEdge'
                        edge['data']['classes'] += ' highlightedEdge'
                        
                    finalEdges.append(edge)
                
            
            for product in value.get('productList',[]):
                if product not in currNodes:
                    currNodes[product] = {
                        'data': {'id': product, 'label':product,'classes' : nodes.get(product,{}).get('class', ''),'parent': [pathway],'link': metabolite_link_map.get(product,'')},
                        'classes': nodes.get(product,{}).get('class', ''),
                    }
                    if product in selected_lipids:
                        currNodes[product]['classes'] += ' highlightedNode'
                        currNodes[product]['data']['classes'] += ' highlightedNode'
                    
                else:
                    if pathway not in currNodes[product]['data']['parent']:
                        currNodes[product]['data']['parent'].append(pathway)
                
                if key not in finalReactionList:
                    edge = {
                        'data': {'source': key, 'target': product, 'classes' : 'second_half','reactInfo' : value.get('reactInfo',''),'reactionType' : value.get('reactionType','')},
                        'classes': 'second_half',
                    }
                    if is_selected_lipid_in_reaction:
                        edge['classes'] += ' highlightedEdge'
                        edge['data']['classes'] += ' highlightedEdge'
                        
                    finalEdges.append(edge)            
            
            #create gene nodes and edges for reaction 
            if key not in finalReactionList:
                reaction_gene_nodes[key] = []
                for gene, modifier in zip(value.get('geneList',[]),value.get('geneModifierType',[])):
                    genecount[gene] = genecount.get(gene, 0) + 1
                    # final_gene_id = f"{gene}_{genecount[gene]}"
                    final_gene_id = f"{key}::gene::{gene}"
                    
                    currNodes[final_gene_id] = {
                        'data': {'id': final_gene_id, 'label':gene,'classes' : nodes.get(gene,{}).get('class', ''),'parent': [pathway],'uniprotAcc': uniprot_cache.get(gene,'')},
                        'classes': nodes.get(gene,{}).get('class', ''),
                    }
                    
                    reaction_gene_nodes[key].append(final_gene_id)
                    
                    edge = {
                        'data': {'source': final_gene_id, 'target': key, 'classes' : modifier,'reactInfo' : value.get('reactInfo',''),'reactionType' : value.get('reactionType','')},
                        'classes': modifier,
                    }
                    if is_selected_lipid_in_reaction:
                        edge['classes'] += ' highlightedEdge'
                        edge['data']['classes'] += ' highlightedEdge'
                        
                    finalEdges.append(edge)  
            
            finalReactionList.add(key)
                

    finalNodes = []
    
    #add lipid nodes to finalNodes
    uniqueParent = set()
    for key, value in currNodes.items():
        #convert parent list to string if multiple parents
        value['data']['parent'] = "_".join(value['data']['parent'])
        uniqueParent.add(value['data']['parent'])
        finalNodes.append(value)
        
    #create parent nodes for lipids with multiple parents
    parentNode = []
    for parent in uniqueParent:
        parentNode.append({
            'data': {'id': parent, 'label':parent,'classes' : 'pathway'},
            'classes': 'pathway',
            # 'selectable': True,
            # 'grabbable': True
        })
                
    return parentNode+finalNodes, finalEdges



def processElements(elements, allowedTissues):

    tfList = set()
    newElements = []
    ##3 first processing edges and making Tf list 
    for ele in elements:
        src = ele.get("data").get("source")
        cl = ele.get("data").get("tissueClass")
        if src is None:
            continue
        
        if cl is None:
            newElements.append({
                'data' : ele.get("data"),
                'classes' : ele.get("data").get("classes")
            })
            continue

        cl = cl.split(" ")
        firstClass = cl[0]
        cl = cl[1:]

        commonTissue = list(allowedTissues & set(cl))
        notAllowed = list(set(cl) - set(commonTissue))

        if len(commonTissue) != 0:
            newClassFormat = [firstClass] + commonTissue
            tfList.add(src)
            # print(newClassFormat)
        else:
            newClassFormat = [firstClass] + notAllowed
        
        newClassFormat = " ".join(newClassFormat)

        # print(src,":",newClassFormat)
        newElements.append({
            'data' : ele.get("data"),
            'classes' : newClassFormat
        })
    # print(tfList)
    #processing nodes
    for ele in elements:
        label = ele.get("data").get("source")
        cl = ele.get("data").get("tissueClass")

        if label:
            continue
        
        if cl is None:
            newElements.append({
                'data' : ele.get("data"),
                'classes' : ele.get("data").get("classes")
            })
            continue
        
        cl = cl.split(" ")
        firstClass = cl[0]
        cl = cl[1:]

        commonTissue = list(allowedTissues & set(cl))
        notAllowed = list(set(cl) - set(commonTissue))

        label = ele.get('data').get('label')

        if label in tfList:
            newClassFormat = [firstClass] + commonTissue
        else:
            newClassFormat = [firstClass] + notAllowed

        newClassFormat = " ".join(newClassFormat)

        # print(label," : ",newClassFormat)
        newElements.append({
            'data' : ele.get("data"),
            'classes' : newClassFormat
        })

    return newElements


def build_dataframe(reactionList):
    dfList = []
    
    id = 1
    
    for reaction, payload in reactionList.items():
        
        pathway = payload['pathways']
        value = payload['value']
        
        reactants = value.get('reactantList')
        products = value.get('productList')
        enzymaticGene =  value.get('geneList')
        
        dfList.append({
            'Rxn' : id,
            'EnzymaticGene' : ", ".join(enzymaticGene),
            'Reactants' : ", ".join(reactants),
            'Products' : ", ".join(products),
            'Pathway' : ", ".join(list(set(pathway)))
        })
        
        id += 1
    
    final_df = pd.DataFrame(dfList)

    columnDefs = [
        {"field": "Rxn", "headerName" : 'No.' ,"maxWidth": 90},
        {"field": "EnzymaticGene", "flex": 1},
        {"field": "Reactants", "flex": 1.5},
        {"field": "Products", "flex": 1.5},
        {"field": "Pathway", "flex": 1},
    ]
    
    return final_df, columnDefs


def elements_to_digraph(elements):
    G = nx.DiGraph()
    
    for ele in elements:
        data = ele.get('data', {})
        source = data.get('source',None)
        target = data.get('target',None)
        
        if source and target:
            G.add_edge(source, target)
        else:
            node_id = data.get('id')
            classes = data.get('classes','')
            
            G.add_node(node_id, classes=classes)
    
    return G


def highlight_elements(elements, selected_lipids):
    
    graph = elements_to_digraph(elements)
    
    rev_graph = graph.reverse(copy=False)
    highlight_nodes = set()
    for t in selected_lipids:
        if t not in rev_graph:
            continue
        # nodes downstream from t
        nodes = nx.descendants(graph, t)
        for node_id in nodes:
            if 'temp' in graph.nodes[node_id].get('classes', '').split():

                # Loop over upstream nodes
                for pred_id in graph.predecessors(node_id):

                    # If predecessor is an enzymatic gene, highlight it
                    if 'enzymaticGene' in graph.nodes[pred_id].get('classes', '').split():
                        highlight_nodes.add(pred_id)

                        
        highlight_nodes.update(nodes)
        
        # nodes upstream that reach t
        highlight_nodes.update(nx.descendants(rev_graph, t))
        highlight_nodes.add(t)
    # highlight edges whose both endpoints are in highlight_nodes
    highlight_edges = {(u, v) for u, v in graph.edges() if u in highlight_nodes and v in highlight_nodes}
    
    node_set = set(highlight_nodes)
    edge_set = set(highlight_edges)

    for el in elements:
        data = el.get('data', {})
        # out = el.copy()
        # classes = out.get('classes', '').split()
        # clear previous highlight/dim classes
        # classes = [c for c in classes if c not in ('highlighted', 'dimmed') and c not in ('highlighted-edge','highlighted-outer','highlighted-inner')]

        if 'source' in data and 'target' in data:  # edge
            key = (data['source'], data['target'])
            if key in edge_set:
                el['classes'] = data.get('classes','') + ' highlighted'
            else:
                el['classes'] = data.get('classes','') + ' dimmed'
    
        else:  # node
            nid = data.get('id')
            if nid in node_set:
                el['classes'] = data.get('classes','') + ' highlighted'
            elif data.get('classes','') != 'pathway':
                el['classes'] = data.get('classes','') + ' dimmed'
    
    return elements




def remove_highlight(elements, selected_lipids):

    for el in elements:
        data = el.get('data', {})
        el['classes'] = data.get('classes','')

    return elements


def populate_table(tf_value, gene_value):
    try:

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
        
        
        # columnDefs = [
        #     {"field": "TF","flex": 1},
        #     {"field": "TargetGene", "headerName" : "EnzymaticGene","flex": 1},
        #     {"field": "Tissue", "flex": 1},
        #     {"field": "Experiment", "headerName":"SPP","flex": 1.5},
        #     {"field": "chea", "flex": 1},
        #     {"field": "Signor", "flex": 1},
        #     {"field": "Trrust", "flex": 1},
        # ]
        
        columnDefs = [
            {"field": "TF", "flex": 1},
            {"field": "TargetGene", "headerName":"EnzymaticGene", "flex": 1},
            {"field": "Tissue", "flex": 1},

            {
                "field": "Experiment",
                "headerName":"SPP",
                "flex": 2,
                "tooltipField": "Experiment",
                "wrapText": False,
                "autoHeight": False,
            },

            {"field": "chea", "flex": 1},
            {"field": "Signor", "flex": 1},
            {"field": "Trrust", "flex": 1},
        ]
                
        # ---- Return for Dash DataTable ----
        return filtered_df.to_dict('records'), columnDefs
    except Exception as e:
        return [],[]
