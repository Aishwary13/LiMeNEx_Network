import os
import json
from functools import lru_cache
import networkx as nx

root_dir = "D:/Raylab/LiMeNEx_Network"

@lru_cache(maxsize=64)
def load_pathway_data(pathway):
    pathway_file = os.path.join(root_dir, 'src/sbmlData/pathwayInfo', f'{pathway}.json')
    with open(pathway_file, 'r') as f:
        pathway_data = json.load(f)
    return pathway_data


def create_nodes_and_edges(pathways,selected_lipids):
    print("Creating nodes and edges...")
    print("Pathways: ", pathways)
    finalNodes = []
    finalEdges = []
    finalNodeSet = set()
    finalReactionList = []
    genecount = {}
    finalLipidNodes = {}
    
    with open(os.path.join(root_dir, 'src/sbmlData/uniprot_cache.json')) as file:
        uniprot_cache = json.load(file)
    
    for pathway in pathways:
        # pathway_file = os.path.join(root_dir, 'src/sbmlData/pathwayInfo', f'{pathway}.json')
        # print("pathway file name : ", pathway_file)
        # pathway_data = json.load(open(pathway_file))

        pathway_data = load_pathway_data(pathway)
        
        nodes = pathway_data.get('nodes', [])
        reactions = pathway_data.get('reactions', [])
        for key,value in reactions.items():
            if key in finalReactionList:
                print(f"Reaction {key} already processed, skipping.")
                continue
            
            finalReactionList.append(key)
            
            #create the connector node for reaction
            finalNodes.append({
                'data': {'id': key, 'label':key,'classes' : 'temp','parent': pathway},
                'classes': 'temp',
            })
            
            intersection = set(selected_lipids).intersection(value.get('reactantList',[]) + value.get('productList',[]))
            if intersection:
                is_selected_lipid_in_reaction = True
            else:
                is_selected_lipid_in_reaction = False
            
            #create node and edges for reaction
            for reactant in value.get('reactantList',[]):
                if reactant not in finalLipidNodes:
                    finalLipidNodes[reactant] = {
                        'data': {'id': reactant, 'label':reactant,'classes' : nodes.get(reactant,{}).get('class', ''),'parent': [pathway]},
                        'classes': nodes.get(reactant,{}).get('class', ''),
                    }
                    
                    if reactant in selected_lipids:
                        finalLipidNodes[reactant]['data']['classes'] += ' highlightedLipid'
                        finalLipidNodes[reactant]['classes'] += ' highlightedLipid'
                else:
                    if pathway not in finalLipidNodes[reactant]['data']['parent']:
                        finalLipidNodes[reactant]['data']['parent'].append(pathway)

                edge = {
                    'data': {'source': reactant, 'target': key, 'classes' : 'first_half','reactInfo' : value.get('reactInfo',''),'reactionType' : value.get('reactionType','')},
                    'classes': 'first_half',
                }
                if is_selected_lipid_in_reaction:
                    edge['classes'] += ' highlightedEdge'
                    edge['data']['classes'] += ' highlightedEdge'
                    
                finalEdges.append(edge)
                
            
            for product in value.get('productList',[]):
                if product not in finalLipidNodes:
                    finalLipidNodes[product] = {
                        'data': {'id': product, 'label':product,'classes' : nodes.get(product,{}).get('class', ''),'parent': [pathway]},
                        'classes': nodes.get(product,{}).get('class', ''),
                    }
                    if product in selected_lipids:
                        finalLipidNodes[product]['classes'] += ' highlightedLipid'
                        finalLipidNodes[product]['data']['classes'] += ' highlightedLipid'
                    
                else:
                    if pathway not in finalLipidNodes[product]['data']['parent']:
                        finalLipidNodes[product]['data']['parent'].append(pathway)
                
                edge = {
                    'data': {'source': key, 'target': product, 'classes' : 'second_half','reactInfo' : value.get('reactInfo',''),'reactionType' : value.get('reactionType','')},
                    'classes': 'second_half',
                }
                if is_selected_lipid_in_reaction:
                    edge['classes'] += ' highlightedEdge'
                    edge['data']['classes'] += ' highlightedEdge'
                    
                finalEdges.append(edge)            

            for gene, modifier in zip(value.get('geneList',[]),value.get('geneModifierType',[])):
                if gene in finalNodeSet:
                    genecount[gene] += 1
                else:
                    finalNodeSet.add(gene)
                    genecount[gene] = 1
                
                finalNodes.append({
                    'data': {'id': f"{gene}_{genecount[gene]}", 'label':gene,'classes' : nodes.get(gene,{}).get('class', ''),'parent': pathway,'uniprotAcc': uniprot_cache.get(gene,'')},
                    'classes': nodes.get(gene,{}).get('class', ''),
                })
                
                edge = {
                    'data': {'source': f"{gene}_{genecount[gene]}", 'target': key, 'classes' : modifier,'reactInfo' : value.get('reactInfo',''),'reactionType' : value.get('reactionType','')},
                    'classes': modifier,
                }
                if is_selected_lipid_in_reaction:
                    edge['classes'] += ' highlightedEdge'
                    edge['data']['classes'] += ' highlightedEdge'
                    
                finalEdges.append(edge)  
                
                          
    #add lipid nodes to finalNodes
    uniqueParent = set()
    for key, value in finalLipidNodes.items():
        #convert parent list to string if multiple parents
        value['data']['parent'] = "_".join(value['data']['parent'])
        uniqueParent.add(value['data']['parent'])
        finalNodes.append(value)
        
    #create parent nodes for lipids with multiple parents
    for parent in uniqueParent:
        finalNodes.append({
            'data': {'id': parent, 'label':parent,'classes' : 'pathway'},
            'classes': 'pathway',
            # 'selectable': True,
            # 'grabbable': True
        })
                
    return finalNodes, finalEdges



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
    import pandas as pd
    root_dir = "D:/Raylab/LiMeNEx_Network"
    dfList = []
    
    id = 1
    
    for reaction, pathway in reactionList.items():
        info = reaction.split(";")
        reactants = info[0][2:].split("|")
        products = info[1][2:].split("|")
        enzymaticGene = info[2][2:].split("|")
        
        dfList.append({
            'Rxn' : id,
            'EnzymaticGene' : ", ".join(enzymaticGene),
            'Reactants' : ", ".join(reactants),
            'Products' : ", ".join(products),
            'Pathway' : ", ".join(pathway)
        })
        
        id += 1
    
    final_df = pd.DataFrame(dfList)
    return final_df


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