from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import smtplib
from email.message import EmailMessage

# dash.register_page(__name__, path='/contact')
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# def send_email_to_user(recipient_email, subject, content):

#     # Sender email credentials
#     sender_email = "limenex.raylab@iiitd.ac.in"
#     sender_password = "hgqnynbduiqijtpo"

#     # Create a MIME message
#     msg = MIMEMultipart("alternative")
#     msg["From"] = sender_email
#     msg["To"] = recipient_email
#     msg["Subject"] = subject

#     # Attach the HTML content
#     msg.attach(MIMEText(content, "html"))

#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Replace with your SMTP server
#             server.starttls()  # Enable secure connection
#             server.login(sender_email, sender_password)  # Login
#             server.sendmail(sender_email, recipient_email, msg.as_string())  # Send email

#         print(f"Email sent successfully to {recipient_email}")
#         return True, "Email sent successfully."
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return False, str(e)

# def send_email_to_user(recipient_email, subject, content):
#     try:
#         # Create SMTP session
#         s = smtplib.SMTP('smtp.gmail.com', 587)
#         # Start TLS for security
#         s.starttls()
#         # Authentication
#         sender_email = "limenex.raylab@iiitd.ac.in"
#         sender_password = "hgqnynbduiqijtpo"  # Note: Store this securely using environment variables
#         s.login(sender_email, sender_password)
        
#         # Prepare the email message
#         email_message = EmailMessage()
#         email_message['From'] = sender_email
#         email_message['To'] = recipient_email
#         email_message['Subject'] = subject
#         email_message.set_content(content)
        
#         # Send the email
#         s.send_message(email_message)
#         # Terminate the session
#         s.quit()
#         return True, "Email sent successfully."
#     except Exception as e:
#         return False, str(e)


# # Callback function
# @callback(
#     Output("email-status", "children"),
#     Input("send-email", "n_clicks"),
#     State("userName", "value"),
#     State("userEmail", "value"),
#     State("userPhone", "value"),
#     State("userMessage", "value"),
#     prevent_initial_call=True
# )
# def send_email(n_clicks, name, email, phone, message):
#     if not name or not email or not phone or not message:
#         return dbc.Alert("Please fill in all fields.", color="danger")
    
#     subject = "Contact Form Submission"
#     content = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    
#     # Call the email sending function
#     success, result_message = send_email_to_user(email, subject, content)
    
#     if success:
#         return dbc.Alert(result_message, color="success")
#     else:
#         return dbc.Alert(f"Failed to send email. Error: {result_message}", color="danger")
    

# layout = html.Div([
#     html.Div(className='container',children=[
#         html.Div(className='form', children=[
#             html.Div(className='contact-info', children=[
#                 html.H3("Let's get in touch", className='title'),
#                 html.P("Contact us with the following details, and fill up the form with the details.", className='text'),
#                 html.Div(className='info', children=[
#                     html.Div(className='social-information', children=[
#                         html.I(className='fa fa-map-marker'),
#                         html.P('Ray Lab, Indraprastha Institute of Information Technology, Delhi, India')
#                     ]),
#                     html.Div(className='social-information', children=[
#                         html.I(className='fa-solid fa-envelope'),
#                         html.P('arjun@iiitd.ac.in')
#                     ])
#                 ])
#             ]),
            
#             html.Div(className='contact-info-form', children=[
#                 html.Span(className='circle one'),
#                 html.Span(className='circle two'),
#                 html.Div( className = 'formDiv',children=[
#                     html.H3('Contact us', className='title'),
#                     html.Div(className='social-input-containers', children=[
#                         dcc.Input(id = 'userName',type='text', name='name', className='input', placeholder='Name')
#                     ]),
#                     html.Div(className='social-input-containers', children=[
#                         dcc.Input(id='userEmail',type='email', name='email', className='input', placeholder='Email')
#                     ]),
#                     html.Div(className='social-input-containers', children=[
#                         dcc.Input(id = 'userPhone', type='tel', name='phone', className='input', placeholder='Phone')
#                     ]),
#                     html.Div(className='social-input-containers textarea', children=[
#                         dcc.Textarea(id = 'userMessage', name='message', className='input', placeholder='Message')
#                     ]),
#                     html.Button('Send', className='btn', id="send-email"),
#                     html.Div(id="email-status",style={"margin-top":"5px"})
#                 ]),
#             ])
#         ])
#     ])
# ], style={'background-color':'#1a1a1a'})


from dash import html

LOGO_IMG = "/mnt/data/Screenshot 2025-10-04 151743.png"  # use this path as uploaded

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

