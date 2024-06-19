from flask import Flask

from web_app import property_controller

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "¡Hola Mundo!"


app.register_blueprint(property_controller)

if __name__ == "__main__":
    app.run(debug=True)
