def validate_user(data):
    if not data.get("name"):
        return False
    return True