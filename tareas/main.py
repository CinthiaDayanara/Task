from flask import Flask, request, jsonify
import redis
import uuid

app = Flask(__name__)

# Redis configuration
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = str(uuid.uuid4())
    redis_client.hmset(task_id, data)
    return jsonify({"id": task_id, "message": "Task created"}), 201

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = redis_client.hgetall(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not redis_client.exists(task_id):
        return jsonify({"error": "Task not found"}), 404
    redis_client.hmset(task_id, data)
    return jsonify({"message": "Task updated"})

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not redis_client.exists(task_id):
        return jsonify({"error": "Task not found"}), 404
    redis_client.delete(task_id)
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
