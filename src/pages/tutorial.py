from dash import html
from typing import List
from dash.development.base_component import Component

def HelpSection(children):
    return html.Div(
        children,
        style={
            "marginBottom": "60px",
            "maxWidth": "1000px",
            "margin": "0 auto",
        }
    )


def SectionHeader(title, subtitle=None):
    return html.Div(
        [
            html.H2(
                title,
                style={
                    "fontSize": "28px",
                    "fontWeight": "700",
                    "marginBottom": "6px",
                },
            ),
            html.P(
                subtitle,
                style={
                    "color": "#b0b0b0",
                    "fontSize": "14px",
                },
            ) if subtitle else None,
            html.Div(
                style={
                    "height": "2px",
                    "width": "60px",
                    "background": "#3b82f5",
                    "marginTop": "12px",
                }
            ),
        ],
        style={"marginTop": "50px"},
    )


    
def StepCard(step_number,header=None ,description=None, points=None):
    points = points or []

    return html.Div(
        [
            # Step header
            html.Div(
                f"Step {step_number} : {header}" if header else f"Step {step_number}",
                style={
                    "fontWeight": "600",
                    "color": "#38bdf8",
                    "fontSize": "15px",
                    "marginBottom": "6px",
                },
            ),

            # Step description (optional)
            html.Div(
                description,
                style={
                    "fontSize": "15px",
                    "color": "#e5e7eb",
                    "lineHeight": "1.6",
                    "marginBottom": "8px",
                },
            ) if description else None,

            # Bullet points (optional)
            html.Ul(
                [
                    html.Li(
                        point,
                        style={
                            "marginBottom": "6px",
                            "color": "#d1d5db",
                            "fontSize": "15px",
                            "lineHeight": "1.5",
                        },
                    )
                    for point in points
                ],
                style={
                    "paddingLeft": "20px",
                    "margin": "0",
                },
            ) if points else None,
        ],
        style={
            "backgroundColor": "#1e1e1e",
            "border": "1px solid #374152",
            "borderRadius": "10px",
            "padding": "16px",
            "marginTop": "14px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.35)",
        },
    )



def FigurePlaceholder(
    src,
    caption=None,
    width="900px",
):
    return html.Div(
        [
            html.Div(
                html.Img(
                    src=src,
                    style={
                        "width": "100%",
                        "height": "auto",      # 👈 key
                        "display": "block",
                        "borderRadius": "8px",
                    },
                ),
                style={
                    "maxWidth": width,
                    "backgroundColor": "#0f172a",
                    "borderRadius": "12px",
                    "border": "1px solid #374152",
                    "boxShadow": "0 8px 24px rgba(0,0,0,0.35)",
                    "padding": "6px",
                },
            ),

            html.Div(
                caption,
                style={
                    "marginTop": "8px",
                    "fontSize": "14px",
                    "color": "#9ca3af",
                    "textAlign": "center",
                    "maxWidth": width,
                },
            ) if caption else None,
        ],
        style={
            "marginTop": "24px",
            "marginBottom" : '18px',
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
        },
    )



def InterpretationPanel(title="Output Interpretation", description=None, items=None):
    items = items or []

    return html.Div(
        [
            # Panel title
            html.Div(
                title,
                style={
                    "fontWeight": "600",
                    "fontSize": "15px",
                    "color": "#38bdf8",
                    "marginBottom": "6px",
                },
            ),

            # Optional description
            html.Div(
                description,
                style={
                    "fontSize": "15px",
                    "color": "#d1d5db",
                    "lineHeight": "1.6",
                    "marginBottom": "12px",
                },
            ) if description else None,

            # Key–Value grid
            html.Div(
                [
                    html.Div(
                        [
                            # Key (left column)
                            html.Div(
                                key,
                                style={
                                    "fontWeight": "600",
                                    "color": "#e5e7eb",
                                    "fontSize": "15px",
                                },
                            ),

                            # Value (right column)
                            html.Div(
                                value,
                                style={
                                    "color": "#d1d5db",
                                    "fontSize": "15px",
                                    "lineHeight": "1.5",
                                    "wordBreak": "break-word",
                                },
                            ),
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "160px 1fr",
                            "columnGap": "12px",
                            "marginBottom": "10px",
                        },
                    )
                    for key, value in items
                ]
            ),
        ],
        style={
            "marginTop": "24px",
            "padding": "16px",
            "borderRadius": "10px",
            "backgroundColor": "#111827",
            "border": "1px solid #374152",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.35)",
        },
    )



from typing import List
from dash.development.base_component import Component


def HelpInputDescription(input_number, description=None):

    children: List[Component] = [
        html.H4(
            f"Input {input_number}",
            style={
                "fontSize": "18px",
                "fontWeight": "500",
                "color": "#e5e7eb",
            },
        )
    ]

    if description and description.strip():
        children.append(
            html.P(
                description,
                className="help-text",
                style={"marginTop": "10px"}
            )
        )

    return html.Div(
        children,
        style={
            "backgroundColor": "#1f2933",
            "border": "1px solid #374152",
            "borderRadius": "12px",
            "padding": "16px",
            "maxWidth": "1000px",
            "margin": "20px auto",
        },
    )

section3 = HelpSection(   
    [
        SectionHeader("C) Console 3:  Enzyme–TF Regulatory Network"),
        HelpInputDescription(input_number=1,description=None
                            ),

        StepCard(1,header=None,description='''
                    Select one or more enzymatic genes of interest or corresponding to 
                    console 2 and click on the option “Fetch TFs” to retrieve corresponding 
                    transcription factors in the regulatory network panel.
                    ''',
                    points=[]
                 ), 
        FigurePlaceholder(src="assets/fig15_15.png",caption=None),
        
        InterpretationPanel(description='''
                           Feature: Console 3 renders a TF–gene regulatory network for the selected 
                            enzymatic genes, displaying the queried genes as green nodes and their 
                            corresponding transcription factors as pink rectangular nodes linked by regulatory 
                            interactions.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig16_16.png",caption=None),
        
    
        InterpretationPanel(description='''
                           Feature:  Filter the TFs regulating the query-associated enzymes by selecting a 
                            Physiological System, such as “Gastrointestinal,” to restrict the TF–gene regulatory 
                            network to that biological context.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig17_17.png",caption=None),
        
        InterpretationPanel(description='''
                            Feature: After selecting a physiological system, choose a tissue (e.g., 
                            Gastrointestinal: stomach) to display only those TF regulators supported for the 
                            query enzymes in that tissue context.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig18_18.png",caption=None),
        
        InterpretationPanel(description='''
                           Feature: The evidence table lists the transcription factors queried for the selected 
                            target genes (e.g., SGMS1 and MGLL) and summarizes their tissue-specific 
                            regulatory interactions supported by SPP evidence, cell-line annotations, and 
                            PubMed literature indexed in ChEA3, TRRUST v2, and SIGNOR, where available.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig19_19.png",caption=None),
    ]
)


section2 = HelpSection(   
    [
        SectionHeader("B) Console 2: Lipid–Enzyme Reaction Exploration"),
        HelpInputDescription(input_number=1,description=None
                            ),

        StepCard(1,header=None,description='''
                    Select one or more enzymatic genes of interest or involved in query lipids 
                    and click on the option “Fetch Reactions” to retrieve corresponding biochemical 
                    reactions in the panel.
                    ''',
                    points=[]
                 ), 
        FigurePlaceholder(src="assets/fig11_11.png",caption=None),
        
        InterpretationPanel(description='''
                            Feature: Selected enzymatic genes are highlighted in sky blue, enabling direct 
                            identification of the queried genes within the reaction-level network.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig12_12.png",caption=None),
        
    
        InterpretationPanel(description='''
                            Feature: For each query, it summarizes the reaction level details of enzymatic 
                            genes in tabular form, enlisting consistent substrates and products, and their 
                            pathways.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig13_13.png",caption=None),
        
        InterpretationPanel(description='''
                            Feature: The reaction network also displays co-participating genes as green 
                            rectangular nodes. Selecting a reaction edge reveals the corresponding biochemical 
                            reaction type (e.g., synthesis, hydrolysis, thiolysis, etc). 
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig14_14.png",caption=None),
    ]
)


section1 = HelpSection(   
    [
        SectionHeader("A) Console 1: Lipid Pathway Network Exploration"),
        HelpInputDescription(input_number=1,description='''This tutorial demonstrates LiMeNEx using a worked example from Ecker 
                                                    et al. (2021), which identified Sphingomyelin (SM) and Triacylglycerol(TG) as 
                                                    robust colorectal cancer-associated lipid signatures.'''
                            ),

        StepCard(1,header="Select lipid of interest",description='''
                    The user can select single or multiple lipids of 
                    interest in Console1 under Multiselect dropdown labelled “Search and Select 
                    Lipids.” We searched Sphingomyelin (SM) and Triacylglycerol (TG) in it.
                    ''',
                    points=[]
                 ), 
        FigurePlaceholder(src="assets/fig2_2.png",caption=None),
        StepCard(2,header="Visualization of metabolic network",points=[
                '''
                 After the user clicks on “Fetch network”, the corresponding pathways of query lipids are automatically rendered.
                '''
                ]),
        
        FigurePlaceholder(src="assets/fig3_3.png",caption =None),
        
        InterpretationPanel(description='''
                            Feature: Queried lipids, central biochemical nodes(Ceramide, Glycerol, 
                            Monoacylglycerol, etc), and non-lipid metabolites are represented by sky blue, 
                            blue, and orange nodes, respectively, to facilitate visual distinction within the 
                            network. It also highlights directly involved biochemical reactions, metabolites and 
                            enzymatic genes via red edges related to query lipids.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig4_4.png",caption=None),
        FigurePlaceholder(src="assets/fig5_5.png"),
        
        HelpInputDescription(input_number=2,description=None),
        
        StepCard(3,header=None,points=[
            '''
                Under “Highlight lipid Centric Pathways” select any single or multiple 
                lipids from the above network and click on option  “Main Chain”
            '''
            ]),
        
        FigurePlaceholder(src="assets/fig6_6.png",caption=None),
        
        
        
        InterpretationPanel(description='''
                            Feature: This option hides the second-level branched chains arising from ceramide 
                            and phosphatidylcholine, retaining only the pathways directly connected to the 
                            queried lipid. The corresponding entities are highlighted as query nodes in sky blue 
                            for clear visual distinction. Selecting the “Full Network” option restores the hidden 
                            branched chains and displays the complete network.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig7_7.png",caption=None),
        
        InterpretationPanel(description='''
                            Feature: Pathway evidence table listing queried lipid species, their associated 
                            pathways, and supporting source databases, with column-wise filtering options.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig8_8.png",caption=None),
        
        InterpretationPanel(description='''
                            Feature: Console 1 network can be exported in SVG, JSON for network graph and 
                            CSV formats for table. Download and refresh controls are provided for saving the 
                            current view and restoring the network visualization.
                            ''',
                            items=[
                            ]),
        
        FigurePlaceholder(src="assets/fig9_9.png",caption=None),
        
        InterpretationPanel(description='''
                                Feature: Interactive legend panel: An expandable legend panel explains the node 
                                types and edge categories used in the network, including query nodes, metabolites, 
                                genes, reaction nodes, substrate/product edges, modifier edges, regulatory edges, 
                                and directly involved reactions.
                                
                                Feature: Metabolite database links: connects metabolite nodes to ChEBI, PubChem 
                                or  KEGG.
                                ''',
                            items=[
                            ]),

        FigurePlaceholder(src="assets/fig10_10.png",caption=None),
        
        InterpretationPanel(description='''                                
                                Feature: Metabolite database links: connects metabolite nodes to ChEBI, PubChem 
                                or  KEGG.
                                ''',
                            items=[
                            ]),
        
        InterpretationPanel(description='''                                
                                Protein database links: connects gene and TF nodes to UniProt.
                                ''',
                            items=[
                            ]),
    ]
)



def HelpSectionDivider():
    return html.Div(
        [
            html.Div(
                "-- Getting Started --",
                style={
                    "fontSize": "36px",
                    "fontWeight": "700",
                    "color": "#3b82f5",
                    "marginBottom": "6px",
                    'textAlign' : "center"
                },
            ),
            html.Div(
                style={
                    "height": "3px",
                    "width": "100%",
                    "backgroundColor": "#374152",
                }
            ),
        ],
        style={
            "maxWidth": "1000px",
            "margin": "60px auto 40px auto",
        },
    )



def HelpIntroBlock():
    return html.Div(
        [
            html.P([
                    '''
                    (LiMeNEx)-Lipid Metabolism Network Explorer is a web server for the 
                    exploration and visualization of Lipid metabolism via biochemical and 
                    transcriptional regulatory networks. It enable users to investigate how lipids, 
                    enzymatic genes and Transcription Factors(TFs) are linked across curated 
                    metabolic pathways. 
                    '''
                    ,
                   
                    html.Br(),html.Br(),
                    '''
                    LiMeNEx is organized into three interconnected consoles: 
                    ''',
                    html.Br(),
                    '''
                    Console 1: Lipid Pathway Network Exploration
                    ''',
                    html.Br(),
                    '''
                    Console 2: Lipid–Enzyme Reaction Exploration 
                    ''',
                    html.Br(),
                    '''
                    Console 3: Enzyme–TF Regulatory Network 
                    '''
                ],
                style={
                    "fontSize": "16px",
                    "lineHeight": "1.7",
                    "color": "#e5e7eb",
                },
            ),

        ],
        style={
            "maxWidth": "1000px",
            "margin": "0 auto 50px auto",
            "padding": "20px",
            "backgroundColor": "#1f2933",
            "borderRadius": "12px",
            "border": "1px solid #374152",
        },
    )


def HelpPageHeader():
    return html.Div(
        [
            html.H1(
                "LiMeNEx Help & Tutorial",
                style={
                    "fontSize": "36px",
                    "fontWeight": "700",
                    "marginBottom": "8px",
                },
            ),
            html.Div(
                style={
                    "height": "3px",
                    "width": "200px",
                    "background": "#3b82f5",
                    "margin": "0 auto",
                }
            ),
        ],
        style={
            "textAlign": "center",
            "marginBottom": "30px",
        },
    )


layout = html.Div(
    [
        HelpPageHeader(),
        html.Div([
            SectionHeader("OverView"),
            ],style={
            "maxWidth": "1000px",
            "margin": "0 auto",
        }),
        FigurePlaceholder(src="assets/fig1_1.png", caption=None),
        HelpIntroBlock(),
        HelpSectionDivider(),
        
        section1,
        section2,
        section3,
        
        html.Div([
                html.Div("© 2026 LiMeNEx — Ray Lab. All rights reserved.", style={"opacity": 0.6}),
            ],
            style={'position':'relative',
                    'bottom':'0px','display' : 'flex',
                    'flexDirection':'column',
                    'textAlign':'center',
                    'justifyContent':'center',
                    'left':'0','width':'100%',
                    'paddingLeft': '3.8em', 
                    'paddingBottom':'10px',
                    'color': 'white',
                    'marginTop': '50px'
            })
    ],
    style={
        "margin": "0 auto",
        "padding": "40px 24px 0px 24px",
        "color": "#ffffff",
        'backgroundColor': "#101010"
    }
)
