from functools import wraps
from fastapi import Request
from datetime import time 

def time_middleware(func):
    @wraps(func)
    def request_time(request: Request):
        return time.time()