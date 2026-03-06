import requests

url = "http://127.0.0.1:5000/api/v1/hello"

response = requests.get(url)

print("Status:", response.status_code)
print("Data:", response.json())