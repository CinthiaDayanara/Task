from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = []
    for key in r.keys('tarea:*'):
        tareas.append(r.hgetall(key))
    return jsonify(tareas)

@app.route('/tareas', methods=['POST'])
def agregar_tarea():
    tarea_id = r.incr('tarea_id')
    tarea = {'id': tarea_id, 'titulo': request.json['titulo']}
    r.hmset(f'tarea:{tarea_id}', tarea)
    return jsonify(tarea), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
