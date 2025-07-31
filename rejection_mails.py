import smtplib
from email.mime.text import MIMEText

APP_PASSWORD = "ebmg cfpb vyih dnmp" #enter password
#for app password ensure the sending mail(company_mail_id) has 2 step verification activated.
#Generate an app password and set it as APP PASSWORD above (it's 16 characters)
def send_rejection_mail(mail_id : str, name : str, role : str, company_name : str, company_mail_id: str):
    subject = f"Regarding Your Application for {role} at {company_name}"
    body = f"Dear {name},\n\nThank you for your interest in the {role} position at {company_name}. We truly appreciate the time and effort you put into your application.\n\nAfter careful consideration, we regret to inform you that you have not been selected to move forward in the recruitment process. This decision was not an easy one due to the high quality of applicants.\n\nWe wish you all the best in your job search and future career.\n\nSincerely,\n\n{company_name} Recruitment Team"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = company_mail_id
    msg["To"] = mail_id

    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(company_mail_id,APP_PASSWORD)
        server.send_message(msg)
    #only for confirmation
    print(f"Email sent to {mail_id}")

#call function with the parameters.
send_rejection_mail(
    mail_id="hormis9919@gmail.com",  # Use a test recipient (e.g. your own)
    name="John Doe",
    role="Backend Developer",
    company_name="TechCorp",
    company_mail_id="videodictator0@gmail.com"
)
