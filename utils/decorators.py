import datetime
from functools import wraps
from .send_email import SendEmail
from flask import request
from config import ALLOWED_iPS


def send_email_decorator(func):
    @wraps(func)
    def send(*args, **kwargs):
        time = datetime.datetime.now()
        subject, text = func(*args, **kwargs)
        text += '\nExecution time: {time}'.format(time=datetime.datetime.now()-time)
        SendEmail().send_email(subject=subject, text=text)
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
