from dash import html

layout = html.Div(
    [
 
        # Page title row
        html.Div(
            [
                html.Div("Contact US", style={"fontSize": "30px", "fontWeight": 700}),
            ],
            style={"marginBottom": "30px","alignItems":"center","display":"flex","justifyContent":"center"}
        ),

        # Cards grid: Contact Card + Map / Visual card + Small support card
        html.Div(
            [
                # ---------- CONTACT CARD ----------
                html.Div(
                    [
                        html.Div("Contact Information", style={"fontSize": "16px", "fontWeight": 700}),
                        html.Div("Official channels for academic collaboration and project support.",
                                    style={"opacity": 0.75, "marginTop": "8px", "fontSize": "14px"}),

                        html.Hr(style={"border": "1px solid #EEEEEE", "marginTop": "14px"}),

                        # Address block
                        html.Div(
                            [
                                html.Div("Address", style={"fontWeight": 600, "marginBottom": "6px"}),
                                html.Div(
                                    "Ray Lab, A-310, R&D Building \n Indraprastha Institute of Information Technology Delhi\nOkhla Industrial Estate, Phase III\nNew Delhi - 110020, India",
                                    style={"whiteSpace": "pre-line", "opacity": 0.9, "fontSize": "14px"}
                                ),
                            ],
                            style={"marginTop": "8px"}
                        ),

                        # Emails block
                        html.Div(
                            [
                                html.Div("Emails", style={"fontWeight": 600, "marginTop": "12px", "marginBottom": "6px"}),
                                html.A("Professor (Prof. Arjun Ray) — arjun@iiitd.ac.in",
                                        href="mailto:arjun@iiitd.ac.in",
                                        style={"display": "block", "color": "#81aedd", "fontSize": "14px", "marginBottom": "6px"}),
                                html.A("Project / Support — limenex.raylab@iiitd.ac.in",
                                        href="mailto:limenex.raylab@iiitd.ac.in",
                                        style={"display": "block", "color": "#93ce96", "fontSize": "14px"}),
                            ]
                        ),

                        # Office hours / small CTA
                        html.Div(
                            [
                                html.Div("Office hours", style={"fontWeight": 600, "marginTop": "14px"}),
                                html.Div("Mon–Fri: 10:00 — 19:00", style={"opacity": 0.85, "fontSize": "14px"}),
                            ]
                        )
                    ],
                    className="shadow-card",
                    style = {"backgroundColor": "#292929",
                             "padding":"15px","borderRadius":"10px",
                             "border" : "1px solid rgba(255,255,255,0.03)",
                             'color' : 'white','boxSizing':'border-box',
                             'width':'450px', 'height': '380px',
                             'overflow':'auto'
                    }
                ),

                # ---------- MAP / VISUAL CARD ----------
                html.Div(
                    [
                        html.Iframe(
                            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2478.3086755312615!2d77.27019371367889!3d28.543995380258337!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390ce3e45d85d3e3%3A0x691393414902968e!2sIIIT-Delhi%20R%26D%20Building!5e0!3m2!1sen!2sin!4v1763767062518!5m2!1sen!2sin",  # <- put the EMBED src here
                            style={
                                "width": "100%",
                                'height' : "100%",
                                "border": "0",
                                "borderRadius": "8px"
                            },
                            title="Location map",
                        )
                    ],
                    className="shadow-card",
                    style = {"backgroundColor": "#292929",
                             "padding":"15px","borderRadius":"10px",
                             "border" : "1px solid rgba(255,255,255,0.03)",
                             'color' : '#fff','boxSizing':'border-box',
                             'width':'450px', 'height': '380px'
                    }
                )
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "flexWrap": "wrap",
                "justifyContent": "center",
                "alignItems": "stretch",
                "gap": "40px",
            }
        ),

        # Footer (small)
        html.Div(
            [
                html.Div("© 2025 LiMeNEx — Ray Lab. All rights reserved.", style={"opacity": 0.6}),
            ],
            style={'position':'absolute','bottom':'0px','display' : 'flex','flexDirection':'column','textAlign':'center','justifyContent':'center','left':'0','width':'100%','paddingLeft': '3.8em', 'paddingBottom':'10px'}
        )
    
    ],
    style={"backgroundColor": "#1a1a1a", "minHeight": "100vh", "padding": "20px 24px", "color": "white"}
)

