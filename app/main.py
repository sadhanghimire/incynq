from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Opportunity(BaseModel):
    value: int
    name: str
    potential: bool

def calculate_score(opportunity: Opportunity) -> int:
    if opportunity.potential:
        return opportunity.value * 2
    return opportunity.value

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/opportunity/")
def create_opportunity(opportunity: Opportunity):
    if calculate_score(opportunity) > 100:
        return {"message": f"Opportunity '{opportunity.name}' with value {opportunity.value} created successfully!"}
    else:
        return {"message": f"Opportunity '{opportunity.name}' with value {opportunity.value} is not valuable enough."}