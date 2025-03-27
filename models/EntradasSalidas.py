from config import db
from models.Usuario import Usuarios
from models.Ubicaciones import Ubicacion  # Asegura que esta importación sea correcta

class EntradasSalidas(db.Model):
    __tablename__ = 'entradas_salidas'

    id_horarios = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    id_ubicacion = db.Column(db.Integer, db.ForeignKey('ubicacion.id_ubicacion', ondelete='CASCADE'), nullable=False)
    
    hora_entrada = db.Column(db.Time, nullable=False)
    hora_salida = db.Column(db.Time)

    # Relaciones
    usuario = db.relationship('Usuarios', backref=db.backref('entradas_salidas', cascade="all, delete"))
    ubicacion = db.relationship('Ubicacion', backref=db.backref('entradas_salidas', cascade="all, delete"))

    def __init__(self, id_usuario, id_ubicacion, hora_entrada, hora_salida=None):
        self.id_usuario = id_usuario
        self.id_ubicacion = id_ubicacion
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida

    def to_dict(self):
        return {
            "id_horarios": self.id_horarios,
            "id_usuario": self.id_usuario,
            "id_ubicacion": self.id_ubicacion,
            "hora_entrada": self.hora_entrada.strftime('%H:%M:%S'),
            "hora_salida": self.hora_salida.strftime('%H:%M:%S') if self.hora_salida else None,
        }
