from flask import Flask, request, jsonify, render_template
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, db=1, decode_responses=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    tarea = request.json
    tarea_id = tarea['id']
    redis.set(f'tarea:{tarea_id}', json.dumps(tarea))
    return jsonify({'message': 'Tarea creada'}), 201

@app.route('/tareas/<tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
    tarea = redis.get(f'tarea:{tarea_id}')
    if tarea:
        return jsonify(json.loads(tarea))
    else:
        return jsonify({'message': 'Tarea no encontrada'}), 404

@app.route('/tareas/<tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    tarea = request.json
    redis.set(f'tarea:{tarea_id}', json.dumps(tarea))
    return jsonify({'message': 'Tarea actualizada'})

@app.route('/tareas/<tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    redis.delete(f'tarea:{tarea_id}')
    return jsonify({'message': 'Tarea eliminada'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
