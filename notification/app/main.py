from flask import Flask, request, jsonify, render_template
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, db=2, decode_responses=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/notificaciones', methods=['POST'])
def crear_notificacion():
    notificacion = request.json
    notificacion_id = notificacion['id']
    redis.set(f'notificacion:{notificacion_id}', json.dumps(notificacion))
    return jsonify({'message': 'Notificación creada'}), 201

@app.route('/notificaciones/<notificacion_id>', methods=['GET'])
def obtener_notificacion(notificacion_id):
    notificacion = redis.get(f'notificacion:{notificacion_id}')
    if notificacion:
        return jsonify(json.loads(notificacion))
    else:
        return jsonify({'message': 'Notificación no encontrada'}), 404

@app.route('/notificaciones/<notificacion_id>', methods=['PUT'])
def actualizar_notificacion(notificacion_id):
    notificacion = request.json
    redis.set(f'notificacion:{notificacion_id}', json.dumps(notificacion))
    return jsonify({'message': 'Notificación actualizada'})

@app.route('/notificaciones/<notificacion_id>', methods=['DELETE'])
def eliminar_notificacion(notificacion_id):
    redis.delete(f'notificacion:{notificacion_id}')
    return jsonify({'message': 'Notificación eliminada'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
