import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import random

def random_delay(min_seconds, max_seconds):
    """
    Pauses the execution for a random amount of time between min_seconds and max_seconds.

    Parameters:
        min_seconds (float): Minimum number of seconds to wait.
        max_seconds (float): Maximum number of seconds to wait.
    """
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)

def read_email_conversation(file_path, index):
    """
    Reads a specific email conversation from a text file and returns a tuple with (From, To, Subject, Message Body).
    
    Parameters:
        file_path (str): Path to the text file containing the email conversations.
        index (int): Index of the conversation to read (0-based).
    
    Returns:
        tuple: A tuple containing (From, To, Subject, Message Body) for the specified email conversation.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into individual emails
    emails = content.strip().split('\n---\n')
    
    if index < 0 or index >= len(emails):
        raise IndexError("The specified index is out of range.")
    
    # Get the specific email
    email = emails[index].strip().split('\n')
    
    if len(email) < 4:
        raise ValueError("The email format is incorrect. It must contain From, To, Subject, and Message Body.")
    
    # Extract the details
    from_field = email[0].split(':', 1)[1].strip()
    to_field = email[1].split(':', 1)[1].strip()
    subject = email[3].strip()
    # Join the remaining lines for the message body
    message_body = '\n'.join(email[4:]).strip()
    
    return (from_field, to_field, subject, message_body)

def makeEmail(from_ : str, to_ : str, sub : str, body : str) -> str:
    message = MIMEMultipart("alternative")
    message["From"] = from_
    message["To"] = to_
    message["Subject"] = sub
    part1 = MIMEText(body, "plain")
    message.attach(part1)
    return message.as_string()


smtp_server = "smtp.gmail.com"
port = 587
sender_email = "molem4866@gmail.com"
password = "vpkcayetemuaygcd"  

#mes = makeEmail("mails\BadGuyEmail.txt", "David@gmail.com", "BadGuy@gmail.com")
for i in range(16):
    context = ssl.create_default_context()  
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        mes = read_email_conversation("mails\mail1.txt", i)
        server.sendmail(mes[0], mes[1], makeEmail(mes[0], mes[1], mes[2], mes[3])) #"arielzaken09@gmail.com"
    print("Email " + str(i) + " sent successfully")
    random_delay(40, 120)







