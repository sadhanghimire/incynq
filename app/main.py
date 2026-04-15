from fastapi import FastAPI
from pydantic import BaseModel
import smtplib
import ssl
from email.mime.text import MIMEText
import os

app = FastAPI()

class Opportunity(BaseModel):
    value: int
    name: str
    potential: bool

def calculate_score(opportunity: Opportunity) -> int:
    if opportunity.potential:
        return opportunity.value * 2
    return opportunity.value

def send_email(opportunity: Opportunity):
    port = 465
    sender = "sg2222@msstate.edu"
    receiver = "sg2222@msstate.edu"
    password = os.environ.get("EMAIL_PASSWORD")
    subject = f"Promising Opportunity: {opportunity.name}"
    msg = MIMEText(f"The opportunity '{opportunity.name}' looks promising.")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, reciever, msg.as_string())


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/opportunity/")
def create_opportunity(opportunity: Opportunity):
    if calculate_score(opportunity) > 100:
        send_email(opportunity)
        return {"message": f"Opportunity '{opportunity.name}' with value {opportunity.value} created successfully!"}
    else:
        return {"message": f"Opportunity '{opportunity.name}' with value {opportunity.value} is not valuable enough."}