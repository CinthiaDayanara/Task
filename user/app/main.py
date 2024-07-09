from flask import Flask, request, jsonify, render_template
from redis import Redis
import json

app = Flask(__name__)
redis = Redis(host='redis', port=6379, db=0, decode_responses=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    usuario = request.json
    usuario_id = usuario['id']
    redis.set(f'usuario:{usuario_id}', json.dumps(usuario))
    return jsonify({'message': 'Usuario creado'}), 201

@app.route('/usuarios/<usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = redis.get(f'usuario:{usuario_id}')
    if usuario:
        return jsonify(json.loads(usuario))
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@app.route('/usuarios/<usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    usuario = request.json
    redis.set(f'usuario:{usuario_id}', json.dumps(usuario))
    return jsonify({'message': 'Usuario actualizado'})

@app.route('/usuarios/<usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    redis.delete(f'usuario:{usuario_id}')
    return jsonify({'message': 'Usuario eliminado'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
