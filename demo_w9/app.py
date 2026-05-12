from flask import Flask
from flasgger import Swagger
import yaml

app = Flask(__name__)

# Load file YAML của bạn
with open("openapi.yaml", "r") as f:
    template = yaml.safe_load(f)

swagger = Swagger(app, template=template, config={
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
})

@app.route("/")
def home():
    return "Payment API running"

if __name__ == "__main__":
    app.run(port=3000, debug=True)