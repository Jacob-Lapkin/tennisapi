from models import User
def generate_key():
    import random
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    key = ""
    for i in range(15):
        key += random.choice(chars)
    return key

def check_key(key):
    key = User.query.filter_by(key=key).first()
    if key:
        return True
    else:
        return False
    