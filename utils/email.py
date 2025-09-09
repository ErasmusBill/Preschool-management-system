from django.core.mail import EmailMessage

def send_email(subject, recipient_list, message):
    email_message = EmailMessage(
        subject=subject,
        body=message,            
        to=recipient_list        
    )
    email_message.send()        
    return "Email sent successfully"
