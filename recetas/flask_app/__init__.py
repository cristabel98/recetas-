from flask import Flask

app = Flask(__name__)#inicializamos app

app.secret_key = "llave secretaaa!"  #se necesita para la sesion

app.config["UPLOAD_FOLDER"]="flask_app/static/img"