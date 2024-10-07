import json
from flask import Flask, jsonify, request

app = Flask(__name__)

with open("users.json", "r") as json_file:
    users = json_file.read()

users = json.loads(users)

def find_user(name=None, id=None):
    if name:
        for user in users:
            if user['name'] == name:
                return True, user
    elif id:
        for user in users:
            if user['id'] == id:
                return True, user
    return False, "User not found"

def validate_body(data):
    required_fields = ['name', 'id', 'email']
    for field in required_fields:
        if field not in data:
            return False, f"Missing: Field {field} is missing in the body"
    return True, ""

@app.route("/api/users", methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route("/api/users/<int:id>", methods=['GET'])
def get_user_by_id(id):
    found, details = find_user(id=id)
    if not found:
        return jsonify({"Error": details})
    return jsonify(details)

@app.route("/api/find-name", methods=['GET'])
def get_user_name():
    username = request.args.get("name")

    found, details = find_user(username)

    if not found:
        return jsonify({"Error": details}), 400
    return jsonify(details)

@app.route("/api/find-id/<int:id>", methods=['GET'])
def get_user_id(id):
    found, details = find_user(id=id)
    if not found:
        return jsonify({"Error": details}), 400
    return jsonify(details)

@app.route("/api/add-user", methods=['POST'])
def add_user():
    data = request.get_json()
    is_valid, error_message = validate_body(data)
    
    if not is_valid:
        return jsonify({"Error": error_message}), 400
    elif any(user['id'] == data['id'] for user in users):
        return jsonify({"Error": "User with id {} already exists.".format(data['id'])}), 400
    else:
        users.append(
            {
                'name': data['name'],
                'email': data['email'],
                'id': data['id']
            }
        )

        with open("users.json", "w") as json_file:
            json.dump(users, json_file, indent=4)
        return jsonify({"Output": "User added"}), 200

@app.route("/api/update-user/<int:id>", methods=['PUT'])
def update_user_name(id):
    data = request.get_json()
    if 'name' not in data:
        return jsonify({"Error": "Missing field name"}), 400
    
    found, details = find_user(id=id)
    if not found:
        return jsonify({"Error": details}), 400
    
    details['name'] = data['name']
    with open("users.json", "w") as json_file:
        json.dump(users, json_file, indent=4)
    return jsonify({"Output": "Username updated successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
