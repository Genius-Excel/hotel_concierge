import mailtrap as mt
from django.conf import settings
from decouple import config 
import vonage
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# Send email custom function.
def custom_email_sender(email_address, subject, message, sender_name):
    mail = mt.Mail(
                    sender=mt.Address(email='noreply@easyappz.com', name=sender_name),
                    to=[mt.Address(email=email_address)],
                    subject=subject,
                    text=message,
                    html=None,
                )

    client = mt.MailtrapClient(token=settings.SMTP_API_TOKEN)
    client.send(mail)



VONAGE_API_KEY=config("VONAGE_API_KEY")
VONAGE_API_SECRET=config("VONAGE_API_SECRET")

def custom_sms_sender(sms_sender, sms_recipient, sms_message):
    client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)

    print("Sending SMS")
    try:
        response_data = client.sms.send_message({
            "from": sms_sender,
            "to": sms_recipient,
            "text": sms_message,
        })

        print("SMS Sent success")
        print(response_data)
    except Exception as e:
        print(f"Not sending because: {e}")



# Email sender with HTML template format

def send_email_with_html_template(template_file: str, template_context: dict,
                                email_address: str, subject: str, sender_name: str):
    try:
        template_loader = FileSystemLoader(searchpath=Path(__file__).parent)
        template_env = Environment(loader=template_loader)
        template_file = template_file
        template_file_content = template_env.get_template(template_file)
        template_context = template_context
    except Exception as e:
        return f"Error: {e}"
    
    # embbed context variables in HTML
    html_content = template_file_content.render(template_context)

    # send Employee mail via mailtrap.
    mail = mt.Mail(
        sender=mt.Address(email='noreply@easyappz.com', name=sender_name),
        to=[mt.Address(email=email_address)],
        subject=subject,
        text=None,
        html=html_content,
    )

    client = mt.MailtrapClient(token=settings.SMTP_API_TOKEN)
    client.send(mail)
