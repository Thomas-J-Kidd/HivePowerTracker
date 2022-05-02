import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
    
def send_email(username, email_address):

    port = 465  # For SSL

    # email service constants
    smtp_server = "smtp.gmail.com"
    sender_email = "youremail"  # Enter your address
    password = "youremailpassword"

    # messgae
    subject = username + " YOUR HIVE POWER IS FULL"
    body =  "Hello there: " + username + "\n\nYour hive power is full"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_address
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    text = message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        # log in to email
        server.login(sender_email, password)
        # send email        
        server.sendmail(sender_email, email_address, text)
        print("Sent email to: ", username)

