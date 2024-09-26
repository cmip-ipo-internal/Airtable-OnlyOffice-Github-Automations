import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def email(to_email,subject,body,file_path):
    # Set your SMTP server details
    smtp_host = 'zzzz.wcrp-cmip.org'  
    smtp_port = 587  
    smtp_user = 'YYYY@wcrp-cmip.org'  
    smtp_pass = 'XXXXX'  


    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    try:
        # Open the file in binary mode
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        # Encode the file in base64
        encoders.encode_base64(part)
        
        # Add header to the attachment
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(file_path)}",
        )
        
        # Attach the file to the email message
        msg.attach(part)

    except Exception as e:
        print(f"Failed to attach file. Error: {e}")

    # Send the email via SMTP server
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Upgrade the connection to TLS
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully with attachment!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
