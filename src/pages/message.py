def jobmessage(session_id,step):

    email_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; padding: 10px;">
            <p>Dear User,</p>
            
            <p>Thank you for using <strong>LiMeNEx</strong>.</p>
            
            <p>The <strong> {step} </strong> step has been successfully completed.</p>
            
            <p><strong>Your Session ID:</strong> {session_id}</p>
            
            <p>You can now proceed with further analysis. Please keep this session ID safe for accessing your previous sessions.</p>
            
            <p>Best regards,<br>
            The <strong>LiMeNEx Team</strong></p>
        </body>
    </html>
    """

    return email_content