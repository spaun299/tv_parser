def message_for_email(template='log.html', successfull=True, message=None):
    if not message:
        if successfull:
            message = 'Successfull'
        else:
            message = 'Error, see email'
    return template, dict(message=message)
