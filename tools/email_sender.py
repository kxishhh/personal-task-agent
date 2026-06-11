import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT

class EmailSender:
    """Handles sending emails"""
    
    def __init__(self):
        self.sender_email = SMTP_EMAIL
        self.sender_password = SMTP_PASSWORD
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
    
    def send_email(self, recipient: str, subject: str, body: str, attachments: list = None) -> dict:
        """
        Send an email
        
        Args:
            recipient: Email address of recipient
            subject: Email subject
            body: Email body
            attachments: List of file paths to attach
            
        Returns:
            dict with status and message
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient
            message["Subject"] = subject
            
            # Add body
            message.attach(MIMEText(body, "plain"))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        self._attach_file(message, file_path)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return {
                "status": "success",
                "message": f"Email sent to {recipient}"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}"
            }
    
    def send_email_with_template(self, recipient: str, subject: str, template_body: str, 
                                variables: dict = None) -> dict:
        """Send email with template variable substitution"""
        body = template_body
        
        if variables:
            for key, value in variables.items():
                body = body.replace(f"{{{{{key}}}}}", str(value))
        
        return self.send_email(recipient, subject, body)
    
    def send_bulk_email(self, recipients: list, subject: str, body: str) -> dict:
        """Send the same email to multiple recipients"""
        results = []
        
        for recipient in recipients:
            result = self.send_email(recipient, subject, body)
            results.append({
                "recipient": recipient,
                "status": result["status"]
            })
        
        return {
            "status": "success",
            "message": f"Bulk email sent to {len(recipients)} recipients",
            "results": results
        }
    
    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach a file to the message"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(file_path)}"
            )
            message.attach(part)
        except Exception as e:
            print(f"Warning: Could not attach file {file_path}: {str(e)}")
