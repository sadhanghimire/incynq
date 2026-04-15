from fastapi import FastAPI
from pydantic import BaseModel
import smtplib
import ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = FastAPI()

class Opportunity(BaseModel):
    value: int
    name: str
    potential: bool

def calculate_score(opportunity: Opportunity) -> int:
    if opportunity.potential:
        return opportunity.value * 2
    return opportunity.value

def send_email(accepted_opportunities: list[str]):
    port = 465
    sender = os.environ.get("EMAIL_SENDER")
    receiver = os.environ.get("EMAIL_RECEIVER")
    password = os.environ.get("EMAIL_PASSWORD")
    
    subject = f"List of Promising Opportunities."
    msg = MIMEText(f"The following opportunities look promising: \n'{accepted_opportunities}'.")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/opportunity/")
def create_opportunity(opportunities: list[Opportunity]):
    accepted_opportunities = []
    for opp in opportunities:
        if calculate_score(opp) > 500:
            accepted_opportunities.append(opp.name)
    if accepted_opportunities:
        send_email(accepted_opportunities)
    return {"accepted_opportunities": accepted_opportunities}