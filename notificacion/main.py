from flask import Flask, request, jsonify, render_template
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, db=2, decode_responses=True)


@app.route('/notification', methods=['POST'])
def crear_notification():
    notification = request.json
    notification_id = notification['id']
    redis.set(f'notification:{notification_id}', json.dumps(notification))
    return jsonify({'message': 'Notificación creada'}), 201

@app.route('/notification/<notification_id>', methods=['GET'])
def obtener_notification(notification_id):
    notification = redis.get(f'notification:{notification_id}')
    if notification:
        return jsonify(json.loads(notification))
    else:
        return jsonify({'message': 'Notificación no encontrada'}), 404

@app.route('/notification/<notification_id>', methods=['PUT'])
def actualizar_notificacion(notification_id):
    notification = request.json
    redis.set(f'notification:{notification_id}', json.dumps(notification))
    return jsonify({'message': 'Notificación actualizada'})

@app.route('/notification/<notification_id>', methods=['DELETE'])
def eliminar_notificacion(notification_id):
    redis.delete(f'notification:{notification_id}')
    return jsonify({'message': 'Notificación eliminada'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
