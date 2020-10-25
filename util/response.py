def ok(message='Ok'):
    return {'status': 'Ok', 'message': message}

def error(message='Error occured'):
    return {'status': 'Error', 'message': message}