from models.EntradasSalidas import EntradasSalidas
from flask import jsonify
from config import db

# Obtener todas las entradas y salidas
def get_all_entradas_salidas():
    try:
        return [es.to_dict() for es in EntradasSalidas.query.all()]
    except Exception as error:
        print(f"ERROR {error}")

# Crear una entrada o salida
def create_entrada_salida(id_usuario, id_ubicacion, hora_entrada, hora_salida):
    try:
        new_es = EntradasSalidas(id_usuario, id_ubicacion, hora_entrada, hora_salida)
        db.session.add(new_es)
        db.session.commit()
        return new_es.to_dict()
    except Exception as e:
        print(f"ERROR {e}")

# Actualizar una entrada o salida
def update_entrada_salida(id_horarios, id_usuario, id_ubicacion, hora_entrada, hora_salida):
    try:
        es = EntradasSalidas.query.get(id_horarios)
        if not es:
            return None

        es.id_usuario = id_usuario
        es.id_ubicacion = id_ubicacion
        es.hora_entrada = hora_entrada
        es.hora_salida = hora_salida
        db.session.commit()

        return es.to_dict()
    except Exception as e:
        print(f"ERROR {e}")

# Eliminar una entrada o salida
def delete_entrada_salida(id_horarios):
    try:
        es = EntradasSalidas.query.get(id_horarios)
        if not es:
            return jsonify({"error": "Registro not found"})
        db.session.delete(es)
        db.session.commit()
        return jsonify({"message": "Registro deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"ERROR {e}")

# Obtener una entrada o salida específica
def get_entrada_salida(id_horarios):
    try:
        es = EntradasSalidas.query.get(id_horarios)
        return es.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
