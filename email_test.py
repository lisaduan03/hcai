import schedule
import time
import smtplib
from email.mime.text import MIMEText
from langchain_ollama import ChatOllama

# Using langchain to call model
# default is 3b parameters but i'm using 1b (1.3 GB)
llm = ChatOllama(model="llama3.2:1b", temperature=0.7)

# Email details
subject = "Health Insurance Claim Update"
sender = "lisajingd@gmail.com"
recipients = ["lisa_duan@brown.edu"]
password = "tcux deup ocfp bsyw"  # Replace with your app-specific password

# reading from files 
def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# generating appeal letter. play around with prompt here!
def generate_appeal(denial_content, patient_notes_content):
    prompt = f"""
    The following is a health insurance claim denial and corresponding patient visit notes. Please generate a formal letter from the perspective of the provider appealing the claim denial using the visit notes, including patient information and medical history.

    --- Health Insurance Claim Denial ---
    {denial_content}

    --- Patient Visit Notes ---
    {patient_notes_content}

    Write a brief professional letter appealing the denial:
    """
    
    # generating the text 
    response = llm.invoke(prompt)
    print("Response generated!")
    return response.content


# sending the email 
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Connect to the Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

# calling functions to read in notes and generate appeal letter 
denial_content = read_file('denial.txt')
patient_notes_content = read_file('patientnotes.txt')
appeal_letter = generate_appeal(denial_content, patient_notes_content)

# Save the appeal letter to a .txt file, this is optional 
def save_appeal_letter(appeal_letter):
    with open('appeal_letter.txt', 'w') as file:
        file.write(appeal_letter)
    print("Appeal Letter generated and saved!")
save_appeal_letter(appeal_letter)

# schedule sending the email 
schedule_time = "09:54"
schedule.every().day.at(schedule_time).do(send_email, subject, appeal_letter, sender, recipients, password)
print(f"Scheduled email to be sent at {schedule_time}.")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute-- how to leave this on??