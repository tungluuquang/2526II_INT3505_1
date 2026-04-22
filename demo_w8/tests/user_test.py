from services.user_service import validate_user

def test_validate_user_success():
    data = {"name": "Tung"}
    assert validate_user(data) == True

def test_validate_user_fail():
    data = {}
    assert validate_user(data) == False