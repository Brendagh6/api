from config import db

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    app = db.Column(db.String(100), nullable=False)
    apm = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    sexo = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    huella = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    passw = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre, app, apm, correo, sexo, fecha_nacimiento,fecha_registro, huella, passw, rol):
        self.nombre = nombre
        self.app = app
        self.apm = apm
        self.correo = correo
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.huella = huella
        self.passw = passw
        self.rol = rol
        self.fecha_registro = fecha_registro

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "app": self.app,
            "apm": self.apm,
            "correo": self.correo,
            "sexo": self.sexo,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "huella": self.huella,
            "passw":self.passw,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
            "rol": self.rol,
        }
