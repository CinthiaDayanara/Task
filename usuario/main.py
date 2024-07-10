from flask import Flask, request, jsonify
import redis
import uuid

app = Flask(__name__)

# Configuración de Redis
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = str(uuid.uuid4())
    redis_client.hmset(user_id, data)
    return jsonify({"id": user_id, "message": "Usuario creado"}), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = redis_client.hgetall(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not redis_client.exists(user_id):
        return jsonify({"error": "Usuario no encontrado"}), 404
    redis_client.hmset(user_id, data)
    return jsonify({"message": "Usuario actualizado"})

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not redis_client.exists(user_id):
        return jsonify({"error": "Usuario no encontrado"}), 404
    redis_client.delete(user_id)
    return jsonify({"message": "Usuario eliminado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
