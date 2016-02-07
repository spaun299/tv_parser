import datetime
from functools import wraps
from .send_email import SendEmail


def send_email_decorator(func):
    @wraps(func)
    def send(*args, **kwargs):
        time = datetime.datetime.now()
        subject, text = func(*args, **kwargs)
        text += '\nExecution time: {time}'.format(time=datetime.datetime.now()-time)
        SendEmail().send_email(subject=subject, text=text)
        return func
    return send
