import json
import smtplib, ssl
import time

#SMTP Options
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = 'your-email@gmail.com'
receiver_email = 'receiver-email@gmail.com'
password = 'your-gmail-access-token'

def lambda_handler(event, context):
    print('Sending test email...')
    
    subject = 'CMPE 583'
    msg = f'This is a test e-mail from CMPE 583 lecture! Your MQTT message is: {event["message"]}'

    message = 'Subject: {}\n\n{}'.format(subject, msg)
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=ctx) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        
    print('test email was sent!')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Test succeeded!')
    }
