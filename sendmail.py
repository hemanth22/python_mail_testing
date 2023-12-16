import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import zipfile
import os

API_KEY_HELPER = os.environ.get('API_KEY_HELPER')
SMTP_URL_FINAL = os.environ.get('SMTP_URL_FINAL')
SMTP_PORT = os.environ.get('SMTP_PORT')

def create_zip(files, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        for file in files:
            zip_file.write(file)

reporthtml = subprocess.getoutput("cat report.html")

sender_email = "hemanth22hemu@gmail.com"

receiver_email = "hemanthbitraece@gmail.com"

message = MIMEMultipart("alternative")

message["Subject"] = "Test Report"

message["From"] = sender_email

message["To"] = receiver_email

# Create the plain-text and HTML version of your message    

text = reporthtml
html = reporthtml

part1 = MIMEText(text, "plain")

part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

files_to_attached = ["file1.json","file2.json","file3.json"]
zip_filename = "report.zip"
create_zip(files_to_attached, zip_filename)

    # Attach the zip file
with open(zip_filename, 'rb') as attachment:
    part = MIMEBase('application', 'zip')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={zip_filename}')
    message.attach(part)

with smtplib.SMTP(SMTP_URL_FINAL, SMTP_PORT) as server:
    server.starttls()
    server.login(sender_email, API_KEY_HELPER)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
    server.quit()
    print("Connection Closed")
