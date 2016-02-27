import time
from functools import wraps
from .send_email import SendEmail
from flask import request
from config import ALLOWED_iPS
from .date_and_time import hours_minutes_seconds_from_seconds
from .log import write_to_log


def send_email_decorator(func):
    @wraps(func)
    def send(*args, **kwargs):
        t = time.time()
        subject, text = func(*args, **kwargs)
        text += '\nExecution time: {time}'.format(
            time=hours_minutes_seconds_from_seconds(time.time()-t))
        SendEmail().send_email(subject=subject, text=text)
        write_to_log(message=text)
        return func
    return send


def allow_ip(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.remote_addr in ALLOWED_iPS:
            return func(*args, **kwargs)
        else:
            return "You don't have permissions for this operation"
    return wrapper
