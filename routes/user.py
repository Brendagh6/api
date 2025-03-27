from flask import Blueprint, jsonify, request
from config import db
from controllers.userController import get_all_users, create_user, get_user, update_user, delete_user, get_user_by_email
from controllers.entradasSalidasController import get_all_entradas_salidas,create_entrada_salida,update_entrada_salida,delete_entrada_salida,get_entrada_salida
from controllers.ubicacionController import get_all_ubicaciones,create_ubicacion,update_ubicacion,delete_ubicacion,get_ubicacion
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask_jwt_extended import create_access_token


from datetime import timedelta, datetime

# Función para convertir timedelta a formato HH:MM:SS
def timedelta_to_str(td):
    if isinstance(td, timedelta):
        # Convertir a horas, minutos y segundos
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return td

user_bp = Blueprint('usuarios', __name__)
ubicacion_bp = Blueprint('ubicacion', __name__)
horario_bp = Blueprint('entradasSalidas', __name__)

# Login de usuario

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)
        correo = data.get('correo')
        passw = data.get('passw')

        if not correo or not passw:
            return jsonify({'error': 'Correo y contraseña son obligatorios'}), 400

        usuario = get_user_by_email(correo)

        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        if not usuario.passw:
            return jsonify({'error': 'Contraseña no encontrada en la base de datos'}), 500

        if not check_password_hash(usuario.passw, passw):
            return jsonify({'error': 'Credenciales incorrectas'}), 401

        # Generar token
        token = create_access_token(identity=usuario.correo)

        return jsonify({'message': 'Autenticación exitosa', 'usuario': usuario.correo, 'token': token})

    except Exception as e:
        return jsonify({'error': f'Error en el login: {e}'}), 500

# Rutas de usuarios
@user_bp.route('/', methods=['GET'])
def get_users():
    return jsonify(get_all_users())

@user_bp.route('/<int:id>', methods=['GET'])
def get_single_user(id):
    user = get_user(id)
    return jsonify(user) if user else jsonify({'error': 'Usuario no encontrado'}), 404

@user_bp.route('/', methods=['POST'])
def create_new_user():
    data = request.get_json()
    new_user = create_user(**data)
    return jsonify(new_user), 201

@user_bp.route('/<int:id>', methods=['DELETE'])
def remove_user(id):
    return delete_user(id)

#Update
@user_bp.route('/<int:id>', methods=['PUT'])
def update_user_by_id(id):
    data = request.get_json()
    updated_user = update_user(id, **data)
    return jsonify(updated_user)

# Rutas de ubicaciones
@ubicacion_bp.route('/', methods=['GET'])
def get_ubicaciones():
    return jsonify(get_all_ubicaciones())

@ubicacion_bp.route('/<int:id>', methods=['GET'])
def get_single_ubicacion(id):
    ubicacion = get_ubicacion(id)
    return jsonify(ubicacion) if ubicacion else jsonify({'error': 'Ubicación no encontrada'}), 404

@ubicacion_bp.route('/', methods=['POST'])
def create_new_ubicacion():
    data = request.get_json()
    new_ubicacion = create_ubicacion(**data)
    return jsonify(new_ubicacion), 201

@ubicacion_bp.route('/<int:id>', methods=['DELETE'])
def remove_ubicacion(id):
    return delete_ubicacion(id)

#update
@ubicacion_bp.route('/<int:id>', methods=['PUT'] )
def update_ubi(id):
    data = request.get_json()
    updated_ubicacion = update_ubicacion(id, **data)
    return jsonify(updated_ubicacion)

# Rutas de entradas y salidas
@horario_bp.route('/', methods=['GET'])
def get_horarios():
    return jsonify(get_all_entradas_salidas())

@horario_bp.route('/<int:id>', methods=['GET'])
def get_single_horario(id):
    horario = get_entrada_salida(id)
    return jsonify(horario) if horario else jsonify({'error': 'Registro no encontrado'}), 404

@horario_bp.route('/', methods=['POST'])
def create_new_horario():
    data = request.get_json()
    new_horario = create_entrada_salida(**data)
    return jsonify(new_horario), 201

@horario_bp.route('/<int:id>', methods=['DELETE'])
def remove_horario(id):
    return delete_entrada_salida(id)

#Update
@horario_bp.route('/<int:id>', methods=['PUT'] )
def updatee_hora(id):
    data = request.get_json()
    updated_hora = update_entrada_salida(id, **data)
    return jsonify(updated_hora)




# Importar usuarios
@user_bp.route("/usuarios/importar", methods=["POST"])
def importar_usuarios():
    try:
        data = request.get_json()
        usuarios = data.get("usuarios", [])

        if not isinstance(usuarios, list) or not usuarios:
            return jsonify({"error": "El archivo no contiene datos válidos"}), 400

        valores = [(u["nombre"], u["app"], u["apm"], u["correo"], u["sexo"], u["fecha_nacimiento"], u["rol"]) for u in usuarios]

        sql = "INSERT INTO usuarios (nombre, app, apm, correo, sexo, fecha_nacimiento, rol) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        with db.cursor() as cursor:
            cursor.executemany(sql, valores)
            db.commit()
            return jsonify({"mensaje": "Usuarios importados correctamente", "registros": cursor.rowcount})
    
    except Exception as e:
        return jsonify({"error": "Error al procesar la importación", "detalle": str(e)}), 500

# Importar ubicaciones
@ubicacion_bp.route("/ubicaciones/importar", methods=["POST"])
def importar_ubicaciones():
    try:
        data = request.get_json()
        ubicaciones = data.get("ubicaciones", [])

        if not isinstance(ubicaciones, list) or not ubicaciones:
            return jsonify({"error": "El archivo no contiene datos válidos"}), 400

        valores = [(u["nombre"], u["tipo"]) for u in ubicaciones]

        sql = "INSERT INTO ubicacion (nombre, tipo) VALUES (%s, %s)"
        
        with db.cursor() as cursor:
            cursor.executemany(sql, valores)
            db.commit()
            return jsonify({"mensaje": "Ubicaciones importadas correctamente", "registros": cursor.rowcount})
    
    except Exception as e:
        return jsonify({"error": "Error al procesar la importación", "detalle": str(e)}), 500

# Importar horarios
@horario_bp.route("/horarios/importar", methods=["POST"])
def importar_horarios():
    try:
        data = request.get_json()
        horarios = data.get("horarios", [])

        if not isinstance(horarios, list) or not horarios:
            return jsonify({"error": "El archivo no contiene datos válidos"}), 400

        valores = [(h["id_usuario"], h["id_ubicacion"], h["hora_entrada"], h["hora_salida"]) for h in horarios]

        sql = "INSERT INTO entradas_salidas (id_usuario, id_ubicacion, hora_entrada, hora_salida) VALUES (%s, %s, %s, %s)"
        
        with db.cursor() as cursor:
            cursor.executemany(sql, valores)
            db.commit()
            return jsonify({"mensaje": "Registros importados correctamente", "registros": cursor.rowcount})
    
    except Exception as e:
        return jsonify({"error": "Error al procesar la importación", "detalle": str(e)}), 500

