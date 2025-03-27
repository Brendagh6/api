from config import db

class Ubicacion(db.Model):
    __tablename__ = 'ubicacion'
    
    id_ubicacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def to_dict(self):
        return {
            "id_ubicacion": self.id_ubicacion,
            "nombre": self.nombre,
            "tipo": self.tipo,
        }
