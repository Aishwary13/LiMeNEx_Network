from dash import html

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


def DescriptionBlock(items):
    return html.Ul(
        [
            html.Li(text, className="desc-bullet")
            for text in items
        ],
        style={
            "color": "#d1d1d1",
            "fontSize": "15px",
            "lineHeight": "1.7",
            "marginTop": "20px",
            "paddingLeft": "22px",   # controls bullet indent
        },
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


def ConsolePurposePanel(
    title="What this console explains",
    description=None,
    points=None,
    footer = None
):
    points = points or []

    return html.Div(
        [
            # Title
            html.Div(
                title,
                style={
                    "fontWeight": "600",
                    "fontSize": "15px",
                    "color": "#22c55e",  # green accent (distinct from blue)
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
                    "marginBottom": "10px",
                },
            ) if description else None,

            # Bullet list
            html.Ul(
                [
                    html.Li(
                        point,
                        style={
                            "marginBottom": "8px",
                            "lineHeight": "1.6",
                        },
                    )
                    for point in points
                ],
                style={
                    "paddingLeft": "18px",
                    "fontSize": "15px",
                    "color": "#e5e7eb",
                },
            ),
            
            html.Div(
                footer,
                style={
                    "fontSize": "15px",
                    "color": "#d1d5db",
                    "lineHeight": "1.6",
                    "marginBottom": "10px",
                },
            ) if footer else None,
        ],
        style={
            "marginTop": "20px",
            "padding": "16px",
            "borderRadius": "10px",
            "backgroundColor": "#0f172a",  # deep slate background
            "border": "1px solid #22c55e55",  # subtle green border
            "boxShadow": "0 4px 12px rgba(0,0,0,0.35)",
        },
    )


def _InterpretationSection(title, content):
    return html.Div(
        [
            html.Div(
                title,
                style={
                    "fontWeight": "600",
                    "color": "#a5b4fc",
                    "marginBottom": "6px",
                    "marginTop": "14px",
                },
            ),
            html.Div(content),
        ]
    )


def _KeyValueRow(label, value):
    return html.Div(
        [
            html.Div(label, className="interp-key"),
            html.Div(value, className="interp-value"),
        ],
        style={
            "display": "grid",
            "gridTemplateColumns": "165px 1fr",
            "columnGap": "12px",
            "marginBottom": "6px",
        },
    )


def _BulletPoint(text):
    return html.Div(
        f"• {text}",
        style={
            "marginBottom": "4px",
            "opacity": 0.9,
        },
    )


def DetailedInterpretationPanel():
    return html.Div(
        [

            # ===== Panel Title =====
            html.Div(
                "Output Interpretation (Console 3)",
                style={
                    "fontSize": "16px",
                    "fontWeight": "600",
                    "color": "#38bdf8",
                    "marginBottom": "12px",
                },
            ),

            # ===== Query Context =====
            _InterpretationSection(
                title="Query Context",
                content=[
                    _KeyValueRow("Query Lipid", "Sphingomyelin"),
                ],
            ),

            # ===== Enzymatic Genes =====
            _InterpretationSection(
                title="Enzymatic Genes Selected",
                content=[
                    _KeyValueRow(
                        "Synthesis Enzymes",
                        "SGMS1, SGMS2 (synthesis enzymes)"
                    ),
                ],
            ),

            # ===== Transcription Factors =====
            _InterpretationSection(
                title="Transcription Factors Identified",
                content=[
                    _KeyValueRow("Global TFs list", "~100+ TFs regulating SGMS1 / SGMS2"),
                    _KeyValueRow(
                        "GI-system specific TFs",
                        "filtered subset ( e.g., EGR1, RELA, GLI2, FOXA2, MAX )"
                    ),
                    _KeyValueRow(
                        "Colon-specific TFs",
                        "further refined subset ( e.g., EGR1, CDX2, GLI2, JUN, ATF2, HOXA4 )"
                    ),
                ],
            ),

            # ===== Tissue Specific Regulation =====
            _InterpretationSection(
                title="Tissue-Specific Regulatory Information (Colon)",
                content=[
                    _KeyValueRow("FOXA2", "Regulates SGMS2"),
                    _KeyValueRow("MAX", "Regulates SGMS1"),
                ],
            ),

            html.Div("This helps in determining which TFs control the synthesis of sphingomyelin in a given tissue.",style={"marginBottom":"10px","marginTop": "16px","fontWeight":"600","fontSize":"14px"}),
            
            # ===== Evidence Table Interpretation =====
            _InterpretationSection(
                title="Evidence Table Insights",
                content=[
                    _BulletPoint("Experimental support (e.g., ChIP-seq, ChIP-IP)"),
                    _BulletPoint("Tissue where validation was observed"),
                    _BulletPoint("Source databases: ChEA3, SIGNOR, TRRUST v2"),
                    _BulletPoint("Tissue specific regulatory pairs of query lipids"),
                ],
            ),
        ],
        style={
            "marginTop": "24px",
            "padding": "18px",
            "borderRadius": "12px",
            "backgroundColor": "#111827",
            "border": "1px solid #374152",
            "fontSize" : "15px",
        },
    )



section3 = HelpSection(
    [
        SectionHeader("C) Console3: Enzyme-TF regulatory Network"),
        StepCard(1,header="Query gene to view TFs:",
                 points =[
                       "The user can select the enzymatic gene corresponding to console 2, identified as the catalyzer of lipid sphingomyelin, under the dropdown “Select gene to view TFs”.",
                       "The user will click on the “fetch TFs” to retrieve all the known TFs of the selected enzymatic gene.",
                       "Hub of TFs pink nodes will appear in console 3 around the selected enzymatic genes SGMS1 and SGMS2 (fig.13)"
                 ]),
        FigurePlaceholder(src="assets/fig12.png",caption="Figure12 : overview of console3(regulatory network)"),
        FigurePlaceholder(src="assets/fig13.png",caption="Figure13 : The enzyme-TF regulating network of sphingomyelin synthesis enzymatic genes SGMS1 and SGMS2, with a hub of Transcription factors regulating them."),
        
        StepCard(2,header="Apply filter:",
                 points=[
                     "The result of TFs regulators of query lipid is restricted to specific physiological systems and tissues such as metabolism, nervous system, gastrointestinal, immune, etc",
                     "Filter the TFS to query lipids by Physiological system by selecting“Gastrointestinal” so that only GI-associated TF regulators appear for enzymes SGMS1 and SGMS2(Fig.14)",
                     '''
                     "Within the Gastrointestinal system, TFs can further be restricted to specific tissues that come under GI (colon, rectum, duodenum, 
                     jejunum, stomach) so we selected the colon, that further filtered and displays only TFs for the enzymatic genes of Sphingomyelin that come within the colon.(Fig.15)"
                     ''',
                 ]),
        FigurePlaceholder(src="assets/fig14.png",caption="Figure 14 : it shows TF regulators of both target genes after filtering by the gastrointestinal system for context-specific exploration of the regulating interactions of sphingomyelin lipid."),
        FigurePlaceholder(src="assets/fig15.png",caption="Figure 15 : It shows TF regulators of both target genes after being filtered by the colon tissue for context-specific exploration of the regulating interactions of sphingomyelin lipid."),
        StepCard(3,header="Evidence table for TF-target gene pairs:",
                 points=[
                     "User can choose any number of TFs for the query gene, say SGMS1 and SGMS2, and click on “load Evidence”",
                     "The evidence table consists of rows TF, Target gene, Tissue and database sources",
                 ]),
        FigurePlaceholder(src="assets/fig16.png",caption='''Figure16 : The evidence table shows all queried transcription factors
                                                associated with the target genes SGMS1 and SGMS2, along with their
                                                regulatory interactions across different tissues supported by tissue-specific
                                                experimental evidence curated from the SPP database, corresponding cell
                                                line studies, and published literature indexed in ChEA3, TRRUSTv2, and
                                                SIGNOR, if available.
                        '''),
        DetailedInterpretationPanel(),
        ConsolePurposePanel(points=[
            "Which transcription factors regulate the enzymatic genes responsible for synthesis/degradation of the query lipid.",
            "Which TFs are tissue-specific, enabling users to link lipid dysregulation to cell-type or tissue-specific regulatory programs.",
            "How transcriptional control may cause upregulation or downregulation of enzymatic genes → influencing lipid levels.",
            "Which TF–gene interactions are experimentally validated, offering stronger biological confidence.",
            "Which TFs may serve as regulatory biomarkers or therapeutic targets for lipid-associated diseases."
        ],footer = '''
                Console-3 reveals the transcriptional regulators of enzymatic
                    genes involved in lipid metabolism by integrating TF–gene
                    interactions across tissues and providing experimentally validated
                    evidence, enabling users to identify tissue-specific regulatory
                    mechanisms underlying lipid biomarker dysregulation.
                '''),
    ]
)

section2 = HelpSection(
    [
        SectionHeader("B) Console 2: Reaction Exploration"),
        FigurePlaceholder(src="assets/fig8.png",caption="Figure 8 : Overview of Console 2(Lipid-gene reactions)"),
        StepCard(1,header="Select the enzymatic gene:",
                 points=[
                     '''
                     User can select sphingomyelin corresponding genes from the drop-down menu under “Select gene for visualization” and tap on 
                     the option ‘fetch reactions’.
                     ''',
                     '''
                     LiMeNEx then extracts and dynamically displays all the reactions corresponding to the selected gene in the Console2.
                     ''',
                     '''
                     For immediate identification of the user, the query gene is designated in sky-blue color, whereas additional enzymes that participate and are 
                     not explicitly queried, displayed in green.(SGMS2, SMPD3 and ENPP7)(Fig.9).
                     ''',
                     '''
                     Tapping on the reaction edge reveals information about the reaction type (Fig. 10). 
                     ''',
                 ]),
        FigurePlaceholder(src="assets/fig9.png",caption='''
                        Figure 9 : It shows Enzymatic gene (SMPD2 and SGMS1) query-driven visualization of reactions associated with sphingomyelin lipid and displays
                        additional genes besides the queried ones, SMPD3 and ENPP7 in sphingomyelin degradation, alongwith SGMS1 for synthesis, designated as green rectangular nodes.
                          '''),
        FigurePlaceholder(src="assets/fig10.png",caption="Figure 10 : It shows an example of type of reaction is hydrolysis, when Ceramide is degraded to sphingomyelin by SMPD2, SMPD3 and ENPP7 enzymes."),
        StepCard(2,header="Reaction table display:",
                 points=[
                    "Console2 displays a detailed summary table for the enzymatic gene query.",
                    '''
                    For each query gene row, the table includes its reactants, products, and pathway information, allowing the user to filter the rows and
                    download the table in CSV format.
                    ''',
                 ]),
        FigurePlaceholder(src="assets/fig11.png",caption="Figure 11: It summarizes the reaction level details of enzymatic genes in tabular form, enlisting consistent substrates and products and the pathways it belongs."),
        InterpretationPanel(description="Sphingomyelin synthesis reaction:",
                            items=[
                                ("Enzymatic gene involved","SGMS1 and SGMS2"),
                                ("Reactants involved","Phosphatidylcholine and Ceramide"),
                                ("Product involved","Sphingomyelin")
                            ]),
        InterpretationPanel(description="Sphingomyelin degradation reaction:",
                            items=[
                                ("Enzymatic gene involved","SMPD1, SMPD2, SMPD3"),
                                ("Reactants involved","Sphingomyelin"),
                                ("Product involved","Ceramide")
                            ]),
        ConsolePurposePanel(points=[
            "What are the reactions in which the query enzymatic genecorresponding to the target lipid participates ?",
            "Is there any other reaction apart from the query lipid reaction in which this query enzymatic gene plays an important role, and in which pathway ?",
            "Directionality of reaction (source to target lipid)",
            "It will help to recognize what are enzymes, metabolites, and reactions behind the target lipid dysregulation in a disease."
        ])
])


section1 = HelpSection(   
    [
        SectionHeader("A) Console 1: Pathway Exploration"),
        DescriptionBlock(["Multiselect dropdown labelled “Search and Select Lipids”",
                          "A checkbox to highlight the directly involved reactions of Lipid pathways.",
                          "Fetch network button to capture pathway networks of the query lipid signature."]),

        FigurePlaceholder(src="assets/fig2.png",caption="Figure 2: The user can select one or multiple lipids in console 1"),
        StepCard(1,header="Select lipid of interest",description='''
                    The User can select more than one lipid query signature, but we took an example of one lipid signature, sphingomyelin (SM),
                    from “The Colorectal Cancer Lipidome: Identification of a Robust Tumor-Specific Lipid Species Signature” (Ecker et al.) 
                    for input in console 1.
                    ''',
                    points=["User can type the query lipid name, and the matching lipid list will appear.",
                            "Click the query lipid, such as sphingomyelin, and click 'Fetch Network'."]
                 ), 
        FigurePlaceholder(src="assets/fig3.png",caption = "Figure 3: Visualization of the query lipid sphingomyelin-associatedmetabolic network"),
        StepCard(2,header="Visualization of network output",points=[
                '''
                After the user clicks on “Fetch network”, the corresponding pathways in which sphingomyelin participates are automatically rendered in 
                their respective white boxes on the right, as you see in Figure 3.
                ''',
                '''
                The Sphingomyelin color-coded with sky-blue query node is also concentrated within the separate white box connected via edges to its 
                distinct metabolic pathways: de novo sphingolipid synthesis pathway and the glycosphingolipid degradation.The pathway 
                names and the respective source of pathways(KEGG, Reactome, Wikipathways or Lipidmaps) corresponding to query lipid appear 
                simultaneously in the black panel on the left.
                ''',
                '''
                Along with the query lipid visualization, LiMeNEx extracts all the shared metabolites among the different metabolic pathways 
                corresponding to the query lipid, just like Ceramide appears besides Sphingomyelin as a central biochemical node, along with directly 
                involved nodes for sphingomyelin via red edges(Fig.4) 
                ''',
                '''
                User can even tap on the green rectangular gene node to get its information from UniProt, whereas metabolite nodes redirect to the 
                CHEBI database or PubChem for further details.
                ''',
                '''
                Highlight the network chain option hides the second level reactions to enhance the entire focus of first level reactions, metabolites and 
                enzymes involved in the query lipid pathways.(Fig.5 and 6)
                ''',
                '''
                On the left panel (Figure.7), the Legends of nodes and edges serve as a visualization guide for the biochemical network components and 
                instinctive navigation of complex gene-metabolite and gene-TF interactions via edges. 
                '''
                ]),
        FigurePlaceholder(src="assets/fig4.png",caption="Figure 4 : It shows directly involved reactions via red edges, metabolites (ceramide and Phosphocholine) related to Sphingomyelin, as well as its corresponding upstream(SGMS1 and SGMS2) and downstream enzymatic genes (SMPD1, SMPD2, SMPD3, and ENPP7) involved."),
        FigurePlaceholder(src="assets/fig5.png"),
        FigurePlaceholder(src="assets/fig6.png",caption="Figures 5 & 6 : represent Console 1 of pathway network exploration with the option enabled “Highlight the main reaction chain” that emphasizes the first-level reactions in gray nodes related to Sphingomyelin and hides downstream or second-level branched chains."),
        FigurePlaceholder(src="assets/fig7.png",caption='''Figure 7 : it represents the legends of nodes and the edges. Nodes are well-defined in distinct shapes and colors, corresponding to the biological
                                                entity. Reaction nodes are separately rendered as squared symbols. Edges designated as biochemical and regulatory interactions that included
                                                substrates, products, modifier edge(enzymes to reactions) and regulatory edges(TF to enzymatic genes). Red-colored edges depict directly involved 
                                                metabolites and reactions in the queried lipid context."
                    '''),
        
        InterpretationPanel(description="Console 1 demonstrates for sphingomyelin:",
                            items=[
                                ("Pathways involved","Denovo sphingolipid synthesis and Glycosphingolipid degradation"),
                                ("Upstream metabolites","Ceramide, Dihydroceramide, Sphinganine,3-ketosphinganine, Palmitoyl-COA"),
                                (" Downstream metabolites","Ceramide"),
                                ("Upstream enzymes","SGMS1, SGMS2, DEGS1, CERS1, KDSR, SPTLC"),
                                ("Downstream enzymes","SMPD, ENPP7"),
                                ("Source of pathways involved","Denovo sphingolipid synthesis(Kegg, Reactome, WikiPathways), Glycosphingolipid degradation(Kegg, Reactome, WikiPathways, LIPIDMAPS)"),
                                ("Type of reaction","acylation, hydrolysis, desaturation, etc"),
                                ("Central hub intermediate metabolites","Ceramide"),
                            ]),
        ConsolePurposePanel(points=[
            "In which lipid metabolism pathway does sphingomyelin issynthesized and degraded ?",
            "Which metabolite act as hub or found commonly in pathways besides sphingomyelin to further understand the metabolic rewiring of diseases like ovarian cancer ?",
            "How can metabolic fluxes of upstream and downstream metabolites and enzymes influence the regulation of query lipids like sphingomyelin ?"
        ])
        
    ]
)




def HelpSectionDivider():
    return html.Div(
        [
            html.Div(
                "-- Tutorial Walkthrough --",
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


def HelpInputDescription():
    return html.Div(
        [
            html.H3(
                "Input Description",
                style={
                    "fontSize": "22px",
                    "fontWeight": "600",
                    "marginBottom": "12px",
                    "color": "#e5e7eb",
                },
            ),

            html.P(
                "For demonstration purposes, we use **Sphingomyelin (SM)** as the input lipid "
                "signature corresponding to colorectal cancer (CRC) disease in the LiMeNEx platform.",
                className="help-text",
            ),

            html.P(
                "This lipid signature serves as the starting point for network construction, "
                "pathway exploration, and downstream interpretation across the different "
                "LiMeNEx consoles described in the following sections.",
                className="help-text",
            ),
        ],
        style={
            "backgroundColor": "#1f2933",
            "border": "1px solid #374152",
            "borderRadius": "12px",
            "padding": "22px",
            "maxWidth": "1000px",
            "margin": "0 auto 50px auto",
        },
    )


def HelpUserExample():
    return html.Div(
        [
            html.H3(
                "Worked Example",
                style={
                    "fontSize": "22px",
                    "fontWeight": "600",
                    "marginBottom": "12px",
                    "color": "#e5e7eb",
                },
            ),

            html.P(
                "In this tutorial, we demonstrate the usability of the LiMeNEx platform "
                "using a worked example derived from a published lipidomics study.",
                className="help-text",
            ),

            html.P(
                "Ecker, Josef, et al. "
                "\"The colorectal cancer lipidome: identification of a robust tumor-specific lipid species signature.\" "
                "Gastroenterology 161.3 (2021): 910–923.",
                style={
                    "fontSize": "14px",
                    "color": "#9ca3af",
                    "fontStyle": "italic",
                    "marginTop": "6px",
                },
            ),

            html.P(
                "In this study, lipidomics profiling was performed on colorectal tumor tissues "
                "versus distal normal tissues to identify lipid species that robustly distinguish "
                "tumor states. Sphingomyelin (SM) and Triglycerides (TG) were identified as "
                "tumor-specific lipid signatures validated across the study cohort.",
                className="help-text",
            ),
        ],
        style={
            "backgroundColor": "#1f2933",
            "border": "1px solid #374152",
            "borderRadius": "12px",
            "padding": "22px",
            "maxWidth": "1000px",
            "margin": "0 auto 30px auto",
        },
    )


def HelpIntroBlock():
    return html.Div(
        [
            html.P([
                    '''
                    (LiMeNEx)-Lipid Metabolism Network Explorer is a web server for the 
                    exploration and visualization of Lipid metabolism gene regulatory networks. 
                    It enables users to query single or multiple lipids considered to be 
                    biomarkers of various metabolic diseases from the perspective of 
                    experimental lipidomics studies. The user can not only identify the 
                    associated pathways of query lipids, but also their upstream and 
                    downstream enzymatic genes that catalyze the reactions involving that lipid 
                    in all the pathways. The platform is equipped with experimentally validated 
                    transcription factors as regulating components of lipids, displayed as 
                    TF-enzyme GRN into a unified network representation. The platform is 
                    consolidated with three exploratory consoles: a network of lipid pathway 
                    metabolites and enzymes, a reaction console to query gene nodes, a 
                    TF-enzyme regulatory network hub filtered by tissues, and the 
                    Physiological system as a latter console.
                    '''
                    ,
                   
                    html.Br(),html.Br(),
                    '''
                    Users can query lipids that have been claimed to be the biomarker from 
                    bulk lipidomics diseased studies to know the regulatory components and 
                    elucidate the cause-and-effect chain from TF to enzyme to lipid 
                    dysregulation in lipid-associated diseases. In this way, lipidomics research 
                    experts will be able to target enzymatic genes, associated TFs, along with 
                    the lipid signatures for diagnosis and prognosis purposes.
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
        # All tutorial sections go here
        HelpIntroBlock(),
        HelpUserExample(),
        HelpInputDescription(),
        FigurePlaceholder(src="assets/fig1.png", caption="Figure1: Overview of Console1(Lipid Pathways Network Exploration)"),
        HelpSectionDivider(),
        
        section1,
        section2,
        section3,
        
        html.Div([
                html.Div("© 2025 LiMeNEx — Ray Lab. All rights reserved.", style={"opacity": 0.6}),
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
