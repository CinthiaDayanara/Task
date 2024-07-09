from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/notificaciones', methods=['GET'])
def obtener_notificaciones():
    notificaciones = []
    for key in r.keys('notificacion:*'):
        notificaciones.append(r.hgetall(key))
    return jsonify(notificaciones)

@app.route('/notificaciones', methods=['POST'])
def agregar_notificacion():
    notificacion_id = r.incr('notificacion_id')
    notificacion = {'id': notificacion_id, 'mensaje': request.json['mensaje']}
    r.hmset(f'notificacion:{notificacion_id}', notificacion)
    return jsonify(notificacion), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
