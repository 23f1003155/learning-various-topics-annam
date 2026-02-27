# tools.py
from datetime import datetime

def get_time():
    return {"time": datetime.now().strftime("%H:%M:%S")}

def echo_message(msg: str):
    return {"echo": msg}
