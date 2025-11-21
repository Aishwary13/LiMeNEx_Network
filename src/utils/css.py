# Define the stylesheet for the Cytoscape graph
ex_stylesheet = [
    # Style for Gene nodes
    {
        'selector': '.transcriptionFactorGene',
        'style': {
            'shape': 'rectangle',
            'background-color': "#d889a0",
            'label': 'data(label)',
            'width': '40px',
            'height': '20px',
            'color': "#000000",
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px',
            'z-index' : 1001
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
            'font-size' : '10px'
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
        'selector' : '.highlightedLipid',
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
            'background-color': '#FF4136',
            'label': 'data(label)',
            'width': '40px',
            'height': '20px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px',
            'z-index' : 1001
        }
    },
    {
        'selector': '.enzymaticGene',
        'style': {
            'shape': 'rectangle',
            'background-color': 'green',
            'label': 'data(label)',
            'width': '40px',
            'height': '20px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    # Style for Lipid nodes
    {
        'selector': '.lipidMetabolite',
        'style': {
            'shape': 'ellipse',
            'background-color': '#0074D9',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': '.nonlipidSubstrate',
        'style': {
            'shape': 'ellipse',
            'background-color': 'orange',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': '.nonlipidMetabolite',
        'style': {
            'shape': 'ellipse',
            'background-color': 'pink',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': '.lipidSubstrate',
        'style': {
            'shape': 'ellipse',
            'background-color': 'red',
            'label': 'data(label)',
            'width': '100px',
            'height': '40px',
            'color': 'black',
            'text-valign': 'center',
            'text-halign': 'center',
            'font-size' : '10px'
        }
    },
    {
        'selector': 'node',
        'style': {'content': 'data(label)'}
    },

    #edges

    {
        'selector': '.reactome',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#000000',
            'label': 'data(label)',
            'font-size': '13px',
            # 'color': '#000000',
            'line-color' : '#07572d'
        }
    },
    {
        'selector': '.overlap',
        'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#000000',
            'label': 'data(label)',
            'font-size': '13px',
            # 'color': '#000000',
            'line-color' : '#800b89'
        }
    }
]