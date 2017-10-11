
class RestErrors(object):
    refused = dict(status_code=1, text='Connection Refused')
    timeout = dict(status_code=1, text='Connection Timeout')
