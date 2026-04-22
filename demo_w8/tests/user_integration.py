def test_create_user_success(client):
    response = client.post("/users", json={"name": "Tung"})
    
    assert response.status_code == 201
    assert response.json["name"] == "Tung"

def test_create_user_fail(client):
    response = client.post("/users", json={})
    
    assert response.status_code == 400
    assert "error" in response.json

def test_get_users(client):
    client.post("/users", json={"name": "A"})
    
    response = client.get("/users")
    
    assert response.status_code == 200
    assert len(response.json) > 0