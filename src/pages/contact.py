from dash import html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import smtplib
from email.message import EmailMessage

# dash.register_page(__name__, path='/contact')
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_to_user(recipient_email, subject, content):

    # Sender email credentials
    sender_email = "limenex.raylab@iiitd.ac.in"
    sender_password = "hgqnynbduiqijtpo"

    # Create a MIME message
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach the HTML content
    msg.attach(MIMEText(content, "html"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Replace with your SMTP server
            server.starttls()  # Enable secure connection
            server.login(sender_email, sender_password)  # Login
            server.sendmail(sender_email, recipient_email, msg.as_string())  # Send email

        print(f"Email sent successfully to {recipient_email}")
        return True, "Email sent successfully."
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False, str(e)

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


# Callback function
@callback(
    Output("email-status", "children"),
    Input("send-email", "n_clicks"),
    State("userName", "value"),
    State("userEmail", "value"),
    State("userPhone", "value"),
    State("userMessage", "value"),
    prevent_initial_call=True
)
def send_email(n_clicks, name, email, phone, message):
    if not name or not email or not phone or not message:
        return dbc.Alert("Please fill in all fields.", color="danger")
    
    subject = "Contact Form Submission"
    content = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    
    # Call the email sending function
    success, result_message = send_email_to_user(email, subject, content)
    
    if success:
        return dbc.Alert(result_message, color="success")
    else:
        return dbc.Alert(f"Failed to send email. Error: {result_message}", color="danger")
    

layout = html.Div([
    html.Div(className='container',children=[
        html.Div(className='form', children=[
            html.Div(className='contact-info', children=[
                html.H3("Let's get in touch", className='title'),
                html.P("Contact us with the following details, and fill up the form with the details.", className='text'),
                html.Div(className='info', children=[
                    html.Div(className='social-information', children=[
                        html.I(className='fa fa-map-marker'),
                        html.P('Ray Lab, Indraprastha Institute of Information Technology, Delhi, India')
                    ]),
                    html.Div(className='social-information', children=[
                        html.I(className='fa-solid fa-envelope'),
                        html.P('arjun@iiitd.ac.in')
                    ])
                ])
            ]),
            
            html.Div(className='contact-info-form', children=[
                html.Span(className='circle one'),
                html.Span(className='circle two'),
                html.Div( className = 'formDiv',children=[
                    html.H3('Contact us', className='title'),
                    html.Div(className='social-input-containers', children=[
                        dcc.Input(id = 'userName',type='text', name='name', className='input', placeholder='Name')
                    ]),
                    html.Div(className='social-input-containers', children=[
                        dcc.Input(id='userEmail',type='email', name='email', className='input', placeholder='Email')
                    ]),
                    html.Div(className='social-input-containers', children=[
                        dcc.Input(id = 'userPhone', type='tel', name='phone', className='input', placeholder='Phone')
                    ]),
                    html.Div(className='social-input-containers textarea', children=[
                        dcc.Textarea(id = 'userMessage', name='message', className='input', placeholder='Message')
                    ]),
                    html.Button('Send', className='btn', id="send-email"),
                    html.Div(id="email-status",style={"margin-top":"5px"})
                ]),
            ])
        ])
    ])
], style={'background-color':'#1a1a1a'})
