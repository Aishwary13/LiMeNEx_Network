import os
import xml.etree.ElementTree as ET
import json

import pandas

dataBasePath= 'D:/Raylab/LiMeNEx_Network/src/sbmlData/networks_updated'
pathwayInfo = "D:/Raylab/LiMeNEx_Network/src/sbmlData/pathwayInfo"

ns = {'celldesigner': 'http://www.sbml.org/2001/ns/celldesigner', '': 'http://www.sbml.org/sbml/level2/version4',
        'html': 'http://www.w3.org/1999/xhtml'}


class stats:
    total_reactions = set()      #
    total_lipids = set()        #
    total_nonlipids = set()       #
    total_product_edges = 0
    total_substrate_edges = 0    
    total_unique_enzymatic_genes = set()  #
    total_modifier_edge = 0
    total_enzymatic_genes = set()
    

def readSbml(fileName,lipid_map):

    # Load and parse the XML file
    filePath = os.path.join(pathwayInfo,fileName)
    print(filePath)
    
    with open(filePath, 'r') as json_file:
        pathway = json.load(json_file)
    # tree = ET.parse(filePath)
    # root = tree.getroot() 
    
    nodes = pathway.get("nodes")

    pathwayName = fileName[:-5]
    for name,value in nodes.items():
        # print(species)
        species_name = name
        className = value.get("class")
        if className != "enzymaticGene":
            if species_name in lipid_map:
                lipid_map[species_name].append(pathwayName)
            else:
                lipid_map[species_name] = [pathwayName]
            
    return lipid_map

lipid_map = {}
for file in os.listdir(os.path.join(pathwayInfo)):
    if file.endswith('.json'):
        lipid_map = readSbml(fileName=file,lipid_map=lipid_map)

print(len(lipid_map))
with open('D:/Raylab/LiMeNEx_Network/src/sbmlData/lipid_pathway_map.json','w') as f:
    json.dump(lipid_map,f,indent=4)
    
    
################################################################################################################

def parseReaction(rx,idToName):
    reactionType = rx.find('.//celldesigner:reactionType', ns).text
    isReversible = rx.get('reversible')
    reactInfo = rx.find('.//html:customInfo', ns)
    if reactInfo is not None:
        infoVar = reactInfo.get('info')
    else:
        infoVar = 'notAssignedInfo'

    reactantList = []
    productList = []
    geneList = []
    geneModifierType = []
    for reactant in rx.findall('.//celldesigner:baseReactant', ns):
        source = reactant.get('species')
        reactantList.append(idToName[source].strip())
    
    for reactant in rx.findall('.//celldesigner:reactantLink', ns):
        source = reactant.get('reactant')
        reactantList.append(idToName[source].strip())

    for product in rx.findall('.//celldesigner:baseProduct', ns):
        target = product.get('species')
        productList.append(idToName[target].strip())
    
    for product in rx.findall('.//celldesigner:productLink', ns):
        target = product.get('product')
        productList.append(idToName[target].strip())

    for modifier in rx.findall('.//celldesigner:modification', ns):
        modifier_species = modifier.get('modifiers')
        modifierType = modifier.get('type')
        geneName  = idToName[modifier_species]
        geneList.append(geneName.strip())
        geneModifierType.append(modifierType)
    
    return {
        'reactionType' : reactionType,
        'isReversible' : isReversible,
        'reactInfo' : infoVar,
        'reactantList' : reactantList,
        'productList' : productList,
        'geneList' : geneList,
        'geneModifierType' : geneModifierType
    }

def processPathway(filePath, count: stats, striped_node: set, actual_node: set):
    reactions = {}
    nodes = {}

    tree = ET.parse(filePath)
    root = tree.getroot()

    genes = []
    for gene in root.findall('.//celldesigner:gene', ns):
        gene_name = gene.get('name').strip()
        genes.append(gene_name)
        count.total_unique_enzymatic_genes.add(gene_name)
        
        # striped_gene = gene_name.strip().replace(" ","").lower()

        # if gene_name not in actual_node and striped_gene in striped_node:
        #     print("[ALERT] Node name Detected -> ",gene_name)
        
        # striped_node.add(striped_gene)
        # actual_node.add(gene_name)
    
    idToName = {}
    for species in root.findall('.//species',ns):
        species_id = species.get('id')
        species_name = species.get('name').strip()

        idToName[species_id] = species_name
         
        nodeClass = species.find('.//html:customClass', ns)
        if nodeClass is not None:
            classVar = nodeClass.get('type').strip()
        else:
            classVar = 'notAssignedNode'
        
        nodes[species_name] = {'id' : species_id, 'class' : classVar}
        
        if 'nonlipid' in classVar:
            count.total_nonlipids.add(species_name)
        elif 'lipid' in classVar:
            count.total_lipids.add(species_name)
        elif 'enzymaticGene' != classVar:
            print(f"Unknown class: {classVar} -> ",species_name)

        striped_name = species_name.strip().replace(" ","").replace("-","").lower()

        if species_name not in actual_node and striped_name in striped_node:
            print(filePath,"  [ALERT] Node name Detected -> ",striped_name)

        striped_node.add(striped_name)
        actual_node.add(species_name)

    for reaction in root.findall('.//reaction', ns):
        reactData = parseReaction(reaction, idToName)

        key = "r=" + "|".join(sorted([temp.lower().replace(" ", "").strip() for temp in reactData['reactantList']]))
        key += (";" + "p=" + "|".join(sorted([temp.lower().replace(" ", "").strip() for temp in reactData['productList']])))
        key += (";" + "g=" + "|".join(sorted([temp.lower().replace(" ", "").strip() for temp in reactData['geneList']])))

        # for temp in reactData['reactantList']:
        #     lipidSet.add(temp)
        # for temp in reactData['productList']:
        #     lipidSet.add(temp) 
        
        reactions[key] = reactData

        #process reactants
        for reactants in reactData["reactantList"]:
            if key not in count.total_reactions:
                count.total_substrate_edges+=1
        
        for product in reactData["productList"]:
            if key not in count.total_reactions:
                count.total_product_edges+=1
                
        for gene in reactData["geneList"]:
            if key not in count.total_reactions:
                count.total_modifier_edge+=1
        
        count.total_reactions.add(key)

    return reactions,nodes


def save_dict_as_json(data_dict, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)  # `indent=4` makes the JSON more readable
    print(f"Dictionary saved to {file_name}")




def runUniqueReactions(networkPath,outputPath):    
    # Iterate over all files in the tfsPath directory
    
    count = stats()
    actual_node = set()
    striped_node = set()
    
    for file_name in os.listdir(networkPath):
        file_path = os.path.join(networkPath, file_name)
        # Check if it's a CSV file
        if os.path.isfile(file_path) and file_name.endswith('.xml'):
            try:
                reactions,nodes = processPathway(file_path, count,actual_node,striped_node)
                data_dict = {
                    'nodes' : nodes,
                    'reactions' : reactions
                }
                path = os.path.join(outputPath,f'{file_name[:-4]}.json')
                save_dict_as_json(data_dict=data_dict,file_name=path)
                
            except Exception as e:
                print(e)
    
    
    import pickle
    with open("src/sbmlData/targetGene.pkl", "wb") as f:
        pickle.dump(list(count.total_unique_enzymatic_genes), f)
    
    
    print(count.total_lipids.intersection(count.total_nonlipids))
    # print(count.total_nonlipids - count.total_lipids)
    
    print(len(count.total_enzymatic_genes))
    print(len(count.total_lipids))
    print(count.total_modifier_edge)
    print(len(count.total_nonlipids))
    print(count.total_product_edges)
    print(len(count.total_reactions))
    print(count.total_substrate_edges)
    print(len(count.total_unique_enzymatic_genes))
    
    return

import pandas as pd
import json
def create_phys_tissue_mapping():
    physiologicalSystemDf = pd.read_csv(os.path.join("D:/Raylab/LiMeNEx_Network/src/sbmlData",'Physiologicalsystem.csv'))
    psToTissue = {}
    for ps in physiologicalSystemDf['Physiological System'].unique():
        psToTissue[ps] = list(physiologicalSystemDf[(physiologicalSystemDf['Physiological System'] == ps)]['Tissue'].unique())
        
    with open('D:/Raylab/LiMeNEx_Network/src/sbmlData/psToTissue.json','w') as f:
        json.dump(psToTissue,f,indent=4)
        
    tissueToPs = {}
    for ps,tissues in psToTissue.items():
        for tissue in tissues:
            if tissue in tissueToPs:
                tissueToPs[tissue].append(ps)
            else:
                tissueToPs[tissue] = [ps]

    with open('D:/Raylab/LiMeNEx_Network/src/sbmlData/tissueToPs.json','w') as f:
        json.dump(tissueToPs,f,indent=4)


def gene_to_reaction():
    
    folder_path = "D:/Raylab/LiMeNEx_Network/src/sbmlData/pathwayInfo"
    gene_to_reactions_map = {}
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                reactions = data.get('reactions', {})
                
                for reaction_key, reaction_data in reactions.items():
                    genes = reaction_data.get('geneList', [])
                    for gene in genes:
                        if gene in gene_to_reactions_map:
                            gene_to_reactions_map[gene][reaction_key] = reaction_data
                            gene_to_reactions_map[gene][reaction_key]['pathways'] = gene_to_reactions_map[gene].get(reaction_key,{}).get('pathways',[]) + [file_name[:-5]]
                        else:
                            gene_to_reactions_map[gene] = {reaction_key: reaction_data}
                            gene_to_reactions_map[gene][reaction_key]['pathways'] = [file_name[:-5]]
    
    json.dump(gene_to_reactions_map, open('D:/Raylab/LiMeNEx_Network/src/sbmlData/gene_to_reactions_map.json','w'), indent=4)
    
    return



def cross_verify_genes():

    mapping_file = 'D:/Raylab/LiMeNEx_Network/src/sbmlData/tf_targetgene_mapping_cleaned.json'
    not_Tf_genes = ["FUT2", "HSD17B8", "PPT1", "AKR1C8","GK3","COX1","COX2"]
    
    pathways_folder = "D:\\Raylab\\LiMeNEx_Network\\src\\sbmlData\\pathwayInfo"
    gene_set = set()
    for file_name in os.listdir(pathways_folder):
        file_path = os.path.join(pathways_folder, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                nodes = data.get('nodes', {})
                
                for node_name, node_data in nodes.items():
                    if "lipid" not in node_data.get('class',''):
                        gene_set.add(node_name)
                        
                        
    with open(mapping_file, 'r') as f:
        tf_target_mapping = json.load(f)
    mapped_genes = set(tf_target_mapping.keys())
    mapped_genes.update(set(not_Tf_genes))
    
    
    # unmapped_genes = gene_set - mapped_genes
    unmapped_genes = mapped_genes - gene_set
    print("Unmapped Genes:")
    print(unmapped_genes)
    
    return


# if __name__ == "__main__":
    # create_phys_tissue_mapping()
    # cross_verify_genes()
    # gene_to_reaction()
    # networkPath = 'D:/Raylab/LiMeNEx_Network/src/sbmlData/networks_updated'
    # outputPath = 'D:/Raylab/LiMeNEx_Network/src/sbmlData/pathwayInfo'
    # runUniqueReactions(networkPath=networkPath,outputPath=outputPath)