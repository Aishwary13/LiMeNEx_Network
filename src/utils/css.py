# Define the stylesheet for the Cytoscape graph
ex_stylesheet = [
    # Style for Gene nodes
    {
        'selector': '.transcriptionFactorGene',
        'style': {
            'shape': 'rectangle',
            'background-color': "#d889a0",
            'label': 'data(label)',
            'width': '50px',
            'height': '20px',
            'color': "#000000",
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px',
            'z-index' : 99,
            'border-color': '#000000',
            'border-width': '1px',
        }
    },
    {
        'selector': '.enzymaticGene',
        'style': {
            'shape': 'rectangle',
            'background-color': '#93ce96',
            'label': 'data(label)',
            'width': '40px',
            'height': '20px',
            'color': '#000000',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px',
            'z-index' : 1000
        }
    },
    # Style for Lipid nodes
    {
        'selector': '.lipidMetabolite\\;first',
        'style': {
            'shape': 'ellipse',
            'background-color': "#81aedd",
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': '#000000',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': '.nonlipidMetabolite\\;first',
        'style': {
            'shape': 'ellipse',
            'background-color': "#f29e65",
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': '#000000',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': '.lipidMetabolite',
        'style': {
            'shape': 'ellipse',
            'background-color': '#81aedd',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': '#000000',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': '.nonlipidMetabolite',
        'style': {
            'shape': 'ellipse',
            'background-color': '#f29e65',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': '#000000',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    # Style for Temp nodes
    {
        'selector': '.temp',
        'style': {
            'shape': 'rectangle',
            'background-color': 'white',  # Set the background color to white
            'border-width': '1px',        # Define the width of the border
            'border-color': 'black',      # Set the border color to black
            'width': '10px',
            'height': '10px',
            'color': '#000000',            # Set the text color to black
            'text-valign': 'center',
            'text-halign': 'center',
        }
    },
    # Style for edges
    {
        'selector': '.second_half',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#000000',
            # 'label': 'data(label)',
            'font-size': '10px',
            # 'color': '#000000',
            'line-color' : '#5B5B5B',
        }
    },
    {
        'selector': '.first_half',
        'style': {
            'curve-style': 'bezier',
            # 'label': 'data(label)',
            'font-size': '10px',
            # 'color': '#000000',
            'line-color' : "#5B5B5B",
        }
    },
    {
        'selector': '.CATALYSIS',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'circle',
            'target-arrow-color': 'black',    # Set the border color of the circle
            'target-arrow-fill': 'hollow',
            # 'target-arrow-size' : '0.6rem',
            # 'line-color': '#2E2E2E',
            # 'label': 'data(label)',
            'font-size': '10px',
            # 'color': '#F5F5F5',
        }
    },
    {
        'selector': '.PHYSICAL_STIMULATION',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': 'blue',    # Set the border color of the circle
            'target-arrow-fill': 'hollow',
            # 'target-arrow-size' : '0.6rem',
            # 'line-color': 'blue',
            # 'label': 'data(label)',
            'font-size': '10px',
            # 'color': '#000000',
        }
    },
    {
        'selector': '.TRANSCRIPTION',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': 'black',    # Set the border color of the circle
            'target-arrow-fill': 'hollow',
            # 'target-arrow-size' : '0.6rem',
            'line-color': 'black',
            'line-style' : 'dashed',
            # 'label': 'data(label)',
            'font-size': '10px',
            'color': '#000000',
        }
    },
    {
        'selector': '.pathway',
        'style': {'content': 'data(label)',
                  'font-size': '40px',
                  'color': '#000000',
                  'border-color': '#000000',
                  'border-width': '2px',
                  'background-color': 'white',
        }
    },
    {
        'selector' : '.highlightedNode',
        'style' : {
            'background-color': "#00E1FF",
        }
    },
    {
        'selector' : '.highlightedEdge',
        'style' : {
            'line-color': "#DB0E0E",
            'width' : 4,
        }
    },
    
    {
        'selector': '.highlighted',
        'style': {
            'opacity': 1,
        }
    },
    {
        'selector': '.dimmed',
        'style': {
            'opacity': 0.2,
        }
    }
    
]


legend_stylesheet = [
    # Node styles
    {
        'selector': '.transcriptionFactorGene',
        'style': {
            'shape': 'rectangle',
            'background-color': '#d889a0',
            'label': 'data(label)',
            'width': '90px',
            'height': '50px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px',
            'z-index' : 1001,
            "font-size":"13px",
            "text-wrap": "wrap",
        }
    },
    {
        'selector': '.enzymaticGene',
        'style': {
            'shape': 'rectangle',
            'background-color': '#93ce96',
            'label': 'data(label)',
            'width': '90px',
            'height': '50px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            "font-size":"13px",
            "text-wrap": "wrap",
        }
    },
    # Style for Lipid nodes
    {
        'selector': '.lipidMetabolite',
        'style': {
            'shape': 'ellipse',
            'background-color': '#81aedd',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            "font-size":"13px",
            "text-wrap": "wrap",
        }
    },
    {
        'selector': '.nonlipidMetabolite',
        'style': {
            'shape': 'ellipse',
            'background-color': '#f29e65',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            "font-size":"13px",
            "text-wrap": "wrap",
        }
    },
    {
        'selector': '.querynode',
        'style': {
            'shape': 'ellipse',
            'background-color': '#00e1ff',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px',
            'z-index' : 1001,
            "font-size":"13px",
            "text-wrap": "wrap",
        }
    },

    {
        'selector': '.temp',
        'style': {
            'label': 'data(label)',
            'shape': 'rectangle',
            'background-color': 'white',  # Set the background color to white
            'border-width': '1px',        # Define the width of the border
            'border-color': 'black',      # Set the border color to black
            'width': '15px',
            'height': '15px',
            'color': '#000000',            # Set the text color to black
            "text-valign": "top",
            "text-halign": "center",
            "text-margin-y": "-4px",
            "font-size":"13px",  
        }
    },
    {
        'selector': '.dummynode',
        'style': {
            'width': '10px',
            'height': '10px',
            'background-color': 'black',
            "text-opacity": 1,
            'background-opacity': 0,
        }
    },
    
    {
        'selector' : 'edge',
        'style' : {
            'label' : 'data(label)',
            "font-size":"13px",
            "text-valign": "top",
            "text-halign": "center",
            "text-margin-y": "-8px",
        }
    },
    
    {
        'selector': '.prod',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#000000',
        }
    },
    
    {
        'selector': '.mod',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'circle',
            'target-arrow-color': 'black',    # Set the border color of the circle
            'target-arrow-fill': 'hollow',
        }
    },
    
    {
        'selector': '.reg',
        'style': {
           'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': 'black',    # Set the border color of the circle
            'target-arrow-fill': 'hollow',
            'line-color': 'black',
            'line-style' : 'dashed',
            'color': '#000000',
        }
    },
    {
        'selector': '.dir',
        'style': {
            'line-color': '#db0d0d',
        }
    },
     {
        'selector': '.parent',
        'style': {
            'label' : 'data(label)'
        }
    },
]

home_page_new_cytoscape_stylesheet = [
    {
        "selector": "edge",
        "style": {
            "curve-style": "unbundled-bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#4ca9ff",            # blue-cyan arrow
            "line-color": "rgba(76,169,255,0.8)",      # #4ca9ff with opacity
            "width": 6,
            "opacity": 0.95,
            "font-size" : "14px",
        },
    },
    
    {
        "selector": ".specialedge",
        "style": {
            "label" : "data(label)",
            "edge-text-rotation": "autorotate",
            "text-wrap": "wrap",
            
            "color": "#f8fafc",
            "curve-style": "unbundled-bezier",      
            "line-color": "transprent", 
            "width": 2,
            "text-opacity": 1,
            "line-opacity": 0,
            "font-size" : "12px",
            
            "control-point-distances": [0],
            "control-point-weights": [0.5],
        },
    },
    
    {
        "selector": ".edge_label",
        "style": {
            "label" : "data(label)",
            "edge-text-rotation": "autorotate",
            "text-wrap": "wrap",
            "color": "white",
            "text-valign": "center",
            "text-halign": "center",
            
            "edge-text-rotation": "none", 
            "color": "#f8fafc",
            
        },
    },
    
    {
        "selector": ".edge_label_pos1",
        "style": {
            "text-margin-x": "80px",
            "text-margin-y": "-8px",
        },
    },
    
    {
        "selector": ".edge_label_pos2",
        "style": {
            "text-margin-y": "-15px",
        },
    },
    {
        "selector": ".edge_label_pos3",
        "style": {
            "text-margin-y": "15pxpx",
        },
    },
    {
        "selector": ".edge_label_pos4",
        "style": {
            "text-margin-x": "-60px",
            "text-margin-y": "-20px",
        },
    },
    
    # curves that bend DOWN (smile)
    {
        "selector": ".down-edge",
        "style": {
            "control-point-distances": [60],
            "control-point-weights": [0.5],
        },
    },
    
    {
        "selector": ".less-down-edge",
        "style": {
            "control-point-distances": [30],
            "control-point-weights": [0.5],
        },
    },
    
    # curves that bend UP (sad)
    {
        "selector": ".up-edge",
        "style": {
            "control-point-distances": [-60],
            "control-point-weights": [0.5],
        },
    },
    
    {
        "selector": ".less-up-edge",
        "style": {
            "control-point-distances": [-30],
            "control-point-weights": [0.5],
        },
    },
    
    # nearly straight for the main chain
    {
        "selector": ".flat-edge",
        "style": {
            "control-point-distances": [0],
            "control-point-weights": [0.5],
        },
    },
    
    {
        "selector": "node",
        "style": {
            "shape": "round-rectangle",
            "background-color": "#18181b",
            "border-width": 2,
            "border-color": "#14e6ff",
            # "border-style": "dashed",     
            "label": "data(label)",
            "color": "#ffffff",
            "font-size": "16px",
            # "font-weight": "500",
            "text-wrap": "wrap",
            "text-max-width": "90px",
            "text-valign": "center",
            "text-halign": "center",
            # "text-margin-y": "-4px",
            "width": "115px",
            "height": "55px",
            "events": "no",
        },
    },
    
    # replace the existing ".parent" block with this
    {
        "selector": ".parent",
        "style": {
            # subtle translucent fill so parent boxes separate from background
            "background-color": "rgba(15,20,30,0.48)",

            # dashed border that uses a cyan-blue accent
            "border-style": "dashed",
            "border-color": "#2ecbff",
            "border-width": 2,

            # keep label but make it a touch bolder & larger
            "label": "data(label)",
            "font-size": "18px",
            "font-weight": "600",
            "color": "#9c4dff",
            
            "padding": "12px",

            # sizing and wrapping
            "height": "88px",
            "text-max-width": "220px",
            "text-wrap": "wrap",
            "text-valign": "center",
            "text-halign": "center",

            # keep it non-interactive
            "events": "no"
        }
    },
    
    {
        "selector": ".special_parent",
        "style": {
            "background-color": "rgba(15,20,30,0.48)",
            "border-style": "dashed",
            "border-color": "#2ecbff",
            "border-width": 1,
            
            "label": "data(label)",
            "font-size": "18px",
            "font-weight": "550",
            "color": "#9c4dff",
            
            "text-wrap": "wrap",
            "text-max-width": "220px",
            "text-valign": "bottom",
            "text-halign": "center",
            # "height" : "100px"   
            "text-margin-y": "4px"         
        }
    },

    # tweak parent label vertical alignment when placed at top
    {
        "selector": ".parent_text_up",
        "style": {
            "text-valign": "top",
            "text-halign": "center",
            "text-margin-y": "-4px"   # small inward padding so text doesn't touch border
        }
    },

    # tweak parent label vertical alignment when placed at bottom
    {
        "selector": ".parent_text_down",
        "style": {
            "text-valign": "bottom",
            "text-halign": "center",
            "text-margin-y": "4px"  # nudge label upward a bit
        }
    },


    {
        "selector" : "#netcomp",
        "style" : {
            "width": "45px",
            "height": "420px",
        }
    },
    {
        "selector" : "#dummy1",
        "style" : {
            'background-opacity': 0,
            'border-opacity': 0, 
            'label': 'data(label)',   
            'text-opacity': 1
        }
    },
    
    {
        "selector" : "#tissues",
        "style" : {
            'background-opacity': 0.85,
            'border-opacity': 0.85,  
            'text-opacity': 1
        }
    },
]