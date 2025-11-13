from flask import Flask, request, jsonify
import pymssql
import sys

DB_CONFIG = {
    'server': '10.14.255.44',
    'database': 'ClinicaNova',
    'user': 'SA',
    'password': 'Shakira123.'
}
app = Flask(__name__)

def get_db_connection():
    """Crea y retorna una nueva conexión a la base de datos."""
    try:
        conn = pymssql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# [GET] /usuarios 
@app.route('/usuarios', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute("SELECT id, nombre, isAdmin FROM Usuario")
        users = cursor.fetchall()
        conn.close()
        return jsonify(users)
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Error al consultar los usuarios: {e}"}), 500

# [GET] id usuario
@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def get_user_by_id(id_usuario):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute("SELECT id, nombre, isAdmin FROM Usuario WHERE id = %d", id_usuario)
        user = cursor.fetchone()
        conn.close()
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Error al consultar el usuario: {e}"}), 500

# [POST] usuario nuevo
@app.route('/usuarios', methods=['POST'])
def create_user():
    new_user_data = request.json
    if not new_user_data or 'nombre' not in new_user_data or 'contrasena' not in new_user_data or 'isAdmin' not in new_user_data:
        return jsonify({"error": "Datos incompletos. Se requiere 'nombre', 'contrasena' y 'isAdmin'."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Usuario (nombre, contrasena, isAdmin) VALUES (%s, %s, %d)"
        cursor.execute(sql, (new_user_data['nombre'], new_user_data['contrasena'], new_user_data['isAdmin']))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Error al crear el usuario: {e}"}), 500

# [PUT] editar usuario
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def update_user(id_usuario):
    update_data = request.json
    if not update_data or 'nombre' not in update_data or 'isAdmin' not in update_data:
        return jsonify({"error": "Datos incompletos. Se requiere 'nombre' y 'isAdmin'."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
    try:
        cursor = conn.cursor()
        sql = "UPDATE Usuario SET nombre = %s, isAdmin = %d WHERE id = %d"
        cursor.execute(sql, (update_data['nombre'], update_data['isAdmin'], id_usuario))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Usuario no encontrado para actualizar"}), 404
            
        conn.close()
        return jsonify({"mensaje": "Usuario actualizado exitosamente"})
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Error al actualizar el usuario: {e}"}), 500

# [DELETE] usuario
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def delete_user(id_usuario):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE id = %d", id_usuario)
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Usuario no encontrado para eliminar"}), 404
            
        conn.close()
        return jsonify({"mensaje": "Usuario eliminado exitosamente"})
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Error al eliminar el usuario: {e}"}), 500

if __name__ == '__main__':
    print("Iniciando API de Usuarios en http://0.0.0.0:5001")
    app.run(host='127.17.0.2', port=5001, debug=True)
