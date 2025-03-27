from models.Ubicaciones import Ubicacion
from flask import jsonify
from config import db

# Obtener todas las ubicaciones
def get_all_ubicaciones():
    try:
        return [ubicacion.to_dict() for ubicacion in Ubicacion.query.all()]
    except Exception as error:
        print(f"ERROR {error}")

# Crear ubicación
def create_ubicacion(nombre, tipo):
    try:
        new_ubicacion = Ubicacion(nombre, tipo)
        db.session.add(new_ubicacion)
        db.session.commit()
        return new_ubicacion.to_dict()
    except Exception as e:
        print(f"ERROR {e}")

# Actualizar ubicación
def update_ubicacion(id_ubicacion, nombre, tipo):
    try:
        ubicacion = Ubicacion.query.get(id_ubicacion)
        if not ubicacion:
            return None

        ubicacion.nombre = nombre
        ubicacion.tipo = tipo
        db.session.commit()

        return ubicacion.to_dict()
    except Exception as e:
        print(f"ERROR {e}")

# Eliminar ubicación
def delete_ubicacion(id_ubicacion):
    try:
        ubicacion = Ubicacion.query.get(id_ubicacion)
        if not ubicacion:
            return jsonify({"error": "Ubicacion not found"})
        db.session.delete(ubicacion)
        db.session.commit()
        return jsonify({"message": "Ubicacion deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"ERROR {e}")

# Obtener ubicación específica
def get_ubicacion(id_ubicacion):
    try:
        ubicacion = Ubicacion.query.get(id_ubicacion)
        return ubicacion.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
