from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = []
    for key in r.keys('usuario:*'):
        usuarios.append(r.hgetall(key))
    return jsonify(usuarios)

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    usuario_id = r.incr('usuario_id')
    usuario = {'id': usuario_id, 'nombre': request.json['nombre']}
    r.hmset(f'usuario:{usuario_id}', usuario)
    return jsonify(usuario), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
