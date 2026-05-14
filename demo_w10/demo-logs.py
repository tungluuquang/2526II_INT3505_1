import logging
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Unstructured Logger
unstructured_logger = logging.getLogger("unstructured")
unstructured_logger.setLevel(logging.INFO)
text_handler = logging.StreamHandler()
text_handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s'))
unstructured_logger.addHandler(text_handler)

# 2. Structured Logger (JSON)
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        if hasattr(record, 'extra_data'):
            log_record.update(record.extra_data)
        return json.dumps(log_record)

structured_logger = logging.getLogger("structured")
structured_logger.setLevel(logging.INFO)
json_handler = logging.StreamHandler()
json_handler.setFormatter(JSONFormatter())
structured_logger.addHandler(json_handler)

logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/unstructured_user', methods=['POST'])
def create_user_unstructured():
    data = request.get_json()
    username = data.get('username', 'unknown')
    email = data.get('email', 'unknown@domain.com')
    role = data.get('role', 'user')
    
    unstructured_logger.info(
        f"Successfully created new user: {username}, email: {email}, assigned role: {role}."
    )
    
    return jsonify({"status": "success", "message": "User created (Unstructured Log)"}), 201


@app.route('/structured_user', methods=['POST'])
def create_user_structured():
    data = request.get_json()
    username = data.get('username', 'unknown')
    email = data.get('email', 'unknown@domain.com')
    role = data.get('role', 'user')
    

    context_data = {
        "event_action": "user_creation",
        "target_username": username,
        "target_email": email,
        "assigned_role": role,
        "status": "success"
    }
    
    structured_logger.info("User created successfully", extra={'extra_data': context_data})
    
    return jsonify({"status": "success", "message": "User created (Structured Log)"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)