from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/v1/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "Hello from Flask Server"
    })

if __name__ == "__main__":
    app.run(debug=True)