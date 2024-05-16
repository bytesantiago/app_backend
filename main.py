from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.adapters.user_repository_adapter_sqlalchemy import \
    UserRepositorySQLAlchemy
from infrastructure.controllers.property_controller import \
    bp as property_controller
from infrastructure.controllers.user_controller import bp as user_controller

# Configuración de la base de datos
DATABASE_URL = "sqlite:///mi_base_de_datos.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "¡Hola Mundo!"


app.register_blueprint(user_controller)
app.register_blueprint(property_controller)

if __name__ == "__main__":
    app.run(debug=True)
