import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileType, FileName, Disposition
from dotenv import load_dotenv
from icecream import ic

class MailService:
    """
    A class that provides methods for sending emails with attachments using SendGrid API.

    Attributes:
        SENDGRID_API_KEY (str): The API key for SendGrid.

    Methods:
        __init__(): Initializes the MailService object and loads the SendGrid API key from environment variables.
        send_email_with_attachment(from_email, to_email, subject, html_content, file_path, file_name): Sends an email with an attachment.

    """

    def __init__(self):
        """
        Initializes the MailService object and loads the SendGrid API key from environment variables.
        """
        load_dotenv()
        self.SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

    def send_email_with_attachment(self, from_email, to_email, subject, html_content, file_path, file_name):
        """
        Sends an email with an attachment.

        Args:
            from_email (str): The email address of the sender.
            to_email (str): The email address of the recipient.
            subject (str): The subject of the email.
            html_content (str): The HTML content of the email.
            file_path (str): The file path of the attachment.
            file_name (str): The name of the attachment file.

        Returns:
            None

        """
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content)

        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()

        attachment = Attachment()
        attachment.file_content = FileContent(encoded)

        file_extension = file_name.split('.')[-1].lower()

        if file_extension == 'epub':
            attachment.file_type = FileType('application/epub+zip')  # EPUB MIME type
        elif file_extension == 'mobi':
            attachment.file_type = FileType('application/x-mobipocket-ebook')  # MOBI MIME type
        else:
            # Default or other file types handling
            attachment.file_type = FileType('application/octet-stream')
        
        attachment.file_name = FileName(file_name)
        attachment.disposition = Disposition('attachment')
        message.attachment = attachment

        try:
            sg = SendGridAPIClient(self.SENDGRID_API_KEY)
            response = sg.send(message)
            ic(response.status_code)
            ic(response.body)
            ic(response.headers)
        except Exception as e:
            ic("Error sending email")
            ic(e)
