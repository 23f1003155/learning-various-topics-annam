# server.py
from fastapi import FastAPI
from tools import get_time, echo_message

app = FastAPI()

@app.get("/tool/time")
def time_tool():
    result = get_time()
    return {
        "tool": "time",
        "result": result
    }

@app.post("/tool/echo")
def echo_tool(data: dict):
    result = echo_message(data["message"])
    return {
        "tool": "echo",
        "result": result
    }
