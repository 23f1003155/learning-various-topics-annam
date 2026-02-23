from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI is running"}

@app.get("/hello")
def hello(name: str = "World"):
    return {"greeting": f"Hello {name}"}

#query params
@app.post("/add")
def add_numbers(a: int, b: int):
    return {"sum": a + b}

#JSON body
class Numbers(BaseModel):
    a: int
    b: int

@app.post("/add-json")
def add_numbers_json(nums: Numbers):
    return {"sum": nums.a + nums.b}
