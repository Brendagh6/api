from models.Usuario import Usuarios
from flask import jsonify
from config import db
from werkzeug.security import generate_password_hash
from datetime import datetime


# Registrar una huella dactilar
def registrar_huella(id_usuario, huella):
    try:
        usuario = Usuarios.query.get(id_usuario)
        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        usuario.huella = huella  # Guardar la huella en texto o base64
        db.session.commit()
        return {"message": "Huella registrada correctamente"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error al registrar huella: {e}"}

# Verificar una huella dactilar
def verificar_huella(huella):
    try:
        usuario = Usuarios.query.filter_by(huella=huella).first()
        if usuario:
            return {"status": "OK", "id_usuario": usuario.id_usuario}
        return {"status": "NO", "message": "Huella no encontrada"}, 404
    except Exception as e:
        return {"error": f"Error al verificar huella: {e}"}



#obtener todo s los ususarios
def get_all_users():
    try:
        return [ user.to_dict() for user in Usuarios.query.all()]    
    except Exception as error:
        print(f"ERROR {error}")
        
        #return jsonify(error)

# Crear usuario

def create_user(nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol, fecha_registro=None):
    try:
        hashed_password = generate_password_hash(passw)  # Hashear contraseña
        
        # Asignar fecha_registro si no se proporciona
        if fecha_registro is None:
            fecha_registro = datetime.utcnow()
        
        new_user = Usuarios(
            nombre=nombre,
            app=app,
            apm=apm,
            correo=correo,
            sexo=sexo,
            fecha_nacimiento=fecha_nacimiento,
            fecha_registro=fecha_registro,
            huella=huella,
            passw=hashed_password,
            rol=rol
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    except Exception as e:
        print(f"ERROR: {e}")
        return None

# Actualizar usuario
def update_user(id_usuario, nombre, app, apm, correo, sexo, fecha_nacimiento,fecha_registro, huella, passw, rol):
    try:
        user = Usuarios.query.get(id_usuario)
        if not user:
            return None

        user.nombre = nombre
        user.app = app
        user.apm = apm
        user.correo = correo
        user.sexo = sexo
        user.fecha_nacimiento = fecha_nacimiento
        user.huella = huella
        user.passw = passw
        user.rol = rol
        user.fecha_registro = fecha_registro
        db.session.commit()

        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")

# Eliminar usuario
def delete_user(id_usuario):
    try:
        user = Usuarios.query.get(id_usuario)
        if not user:
            return jsonify({"error": "User not found"})
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"ERROR {e}")

# Obtener usuario específico
def get_user(id_usuario):
    try:
        user = Usuarios.query.get(id_usuario)
        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        
def get_user_by_email(correo):
    print("Usuario encontrado:", usuario)
    return Usuarios.query.filter_by(correo=correo).first()  # Buscar usuario en la BD
   