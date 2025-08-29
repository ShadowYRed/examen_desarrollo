from flask import Flask, jsonify, request
from models import db
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from views import bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI # conexion a la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS # desactivar el seguimiento de modificaciones

app.register_blueprint(bp) # Registrar el blueprint

if __name__ == '__main__':
    with app.app_context(): # iniciar el contexto de la aplicacion
        db.create_all() # Crear las tablas en la base de datos si no existen
    app.run(debug=True, port=8000)



