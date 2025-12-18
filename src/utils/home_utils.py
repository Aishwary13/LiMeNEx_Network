new_elements = [
    # --- Metabolic layer (middle row) ---
    {
        "data": {"id": "reglayer", "label": "Regulatory Layer"},
        "classes" : "parent parent_text_up"
    },
    {
        "data": {"id": "tf", "label": "345 Transcription Factor","parent" : "reglayer"},
        "position": {"x":90, "y": 110}
    },
    
    {
        "data": {"id": "phys", "label": "Biological System\nCoverage","parent" : "reglayer"},
        "classes" : "special_parent"
    },
    {
        "data": {"id": "tissues", "label": "Tissues",'parent' : 'phys'},
        "position": {"x":290, "y": 110}
    },
    
    {
        "data": {"id": "dummy1", "label": "Physiological Systems",'parent' : 'phys'},
        "position": {"x":290, "y": 160}
    },
    
    {
        "data": {"id": "gene", "label": "330\nGenes",'parent' : 'reglayer'},
        "position": {"x":600, "y": 110}
    },
    
    
    {
        "data": {"id": "metlayer", "label": "Metabolic Layer"},
        "classes" : "parent parent_text_down"
    },
    
    {
        "data": {"id": "lipid", "label": "363\nLipids",'parent' : 'metlayer'},
        "position": {"x":90, "y": 320}
    },
    
    {
        "data": {"id": "nonlipid", "label": "41\nNon-Lipids",'parent' : 'metlayer'},
        "position": {"x":90, "y": 400}
    },
    
    {
        "data": {"id": "metabolite", "label": "404\nMetabolites",'parent' : 'metlayer'},
        "position": {"x":250, "y": 360}
    },
    
    
    {
        "data": {"id": "reaction", "label": "504\nReactions",'parent' : 'metlayer'},
        "position": {"x":600, "y": 360}
    },
    
    
    
    #edges
    {"data": {"source": "tf", "target": "gene","label" : "27345\nTf - Gene Edges\n\nRegulates"},'classes' :"flat-edge edge_label edge_label_pos1"},
    {"data": {"source": "metabolite", "target": "nonlipid"},'classes' :"less-up-edge"},
    {"data": {"source": "metabolite", "target": "lipid"},'classes' :"less-down-edge"},
    {"data": {"source": "metabolite", "target": "reaction", "label" : "557 Substrate Edges"},'classes' :"down-edge edge_label edge_label_pos3"},
    {"data": {"source": "reaction", "target": "metabolite","label" : "530 Product Edges"},'classes' :"down-edge edge_label edge_label_pos2"},
    {"data": {"source": "gene", "target": "reaction","label" : "783\nModifier Edges"},'classes' :"flat-edge edge_label edge_label_pos4"},
    
    
    {"data": {"source": "metabolite", "target": "reaction", "label" : "Reaction produces products\n\n\nReaction uses substrate"},'classes' :"specialedge"},
]
