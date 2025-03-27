from flask import Flask
from config import db, migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Cargar variables de entorno
load_dotenv()


# Crear instancia de Flask
app = Flask(__name__)
app.url_map.strict_slashes = False  # Evita redirecciones automáticas 308

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask import Flask
from config import db, migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Cargar variables de entorno
load_dotenv()

app.config["JWT_SECRET_KEY"] = "tu_clave_secreta"
jwt = JWTManager(app)
# Crear instancia de Flask
app = Flask(__name__)
app.url_map.strict_slashes = False  # Evita redirecciones automáticas 308

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db.init_app(app)
migrate.init_app(app, db)


# Registrar rutas
from routes.user import user_bp, ubicacion_bp, horario_bp

app.register_blueprint(user_bp, url_prefix='/api/usuarios')
app.register_blueprint(ubicacion_bp, url_prefix='/api/ubicaciones')
app.register_blueprint(horario_bp, url_prefix='/api/horarios')

if __name__ == '__main__':
    app.run(debug=True)






