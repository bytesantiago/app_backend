from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.controllers.user_controllers import bp as user_controllers
from infrastructure.adapters.user_repository_adapter_sqlalchemy import UserRepositorySQLAlchemy

# Configuración de la base de datos
DATABASE_URL = "sqlite:///mi_base_de_datos.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola Mundo!'

app.register_blueprint(user_controllers)

@app.before_request
def before_request():
    # Crear una sesión de base de datos para la solicitud
    g.session = Session()

    # Inyectar los repositorios en el contexto global de Flask
    g.user_repository = UserRepositorySQLAlchemy(g.session)

@app.teardown_request
def teardown_request(exception=None):
    # Cerrar la sesión de base de datos al final de la solicitud
    if hasattr(g, 'session'):
        g.session.close()

if __name__ == '__main__':
    app.run(debug=True)
