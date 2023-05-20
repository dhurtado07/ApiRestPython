from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from flask import render_template

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    host="dpg-chk6eo67avj217c84rl0-a",
    database="api_users_5hc8",
    user="nysde",
    password="5u58zQxCYe8TtL1EOQ3V0Uj3gdPWNsde"
)
print("conexion con la DB exitosa")



# Endpoint para crear un usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (cedula_identidad, nombre, primer_apellido, segundo_apellido, fecha_nacimiento)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_usuario
    """, (data['cedula_identidad'], data['nombre'], data['primer_apellido'], data['segundo_apellido'], data['fecha_nacimiento']))
    id_usuario = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Usuario creado', 'id_usuario': id_usuario}), 201


# Endpoint para listar todos los usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id_usuario': usuario[0],
            'cedula_identidad': usuario[1],
            'nombre': usuario[2],
            'primer_apellido': usuario[3],
            'segundo_apellido': usuario[4],
            'fecha_nacimiento': usuario[5].isoformat()
        })
    return jsonify(usuarios_list), 200


# Endpoint para obtener un usuario en específico
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    if usuario:
        usuario_dict = {
            'id_usuario': usuario[0],
            'cedula_identidad': usuario[1],
            'nombre': usuario[2],
            'primer_apellido': usuario[3],
            'segundo_apellido': usuario[4],
            'fecha_nacimiento': usuario[5].isoformat()
        }
        return jsonify(usuario_dict), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404


# Endpoint para actualizar los datos de un usuario
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET cedula_identidad = %s, nombre = %s, primer_apellido = %s, segundo_apellido = %s, fecha_nacimiento = %s
        WHERE id_usuario = %s
    """, (data['cedula_identidad'], data['nombre'], data['primer_apellido'], data['segundo_apellido'], data['fecha_nacimiento'], id_usuario))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Usuario actualizado'}), 200


# Endpoint para eliminar a un usuario
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Usuario eliminado'}), 200


# Endpoint para mostrar el promedio de edades de los usuarios
@app.route('/usuarios/promedio-edad', methods=['GET'])
def promedio_edad_usuarios():
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(EXTRACT(YEAR FROM AGE(fecha_nacimiento))) FROM usuarios")
    promedio_edad = cursor.fetchone()[0]
    cursor.close()
    return jsonify({'promedioEdad': promedio_edad}), 200


# Endpoint para mostrar la versión del API REST
@app.route('/estado', methods=['GET'])
def estado():
    return jsonify({
        'nameSystem': 'api-users',
        'version': '0.0.1',
        'developer': 'Yery Denys Hurtado Mamani',
        'email': 'informatica.live@gmail.com'
    }), 200


# Script para inicializar la base de datos
def init_db():
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario SERIAL PRIMARY KEY,
            cedula_identidad VARCHAR(10) NOT NULL,
            nombre VARCHAR(50) NOT NULL,
            primer_apellido VARCHAR(50) NOT NULL,
            segundo_apellido VARCHAR(50) NOT NULL,
            fecha_nacimiento DATE NOT NULL
        )
    """)
    conn.commit()
    cursor.close()

# Ruta raíz para mostrar la documentación
@app.route('/')
def documentation():
    return render_template('index.html')

# ...

if __name__ == '__main__':
    init_db()
    app.run()
