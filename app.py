#objetivo - Criar uma api de disponibilize a consulta e retorne stats do jogador
from flask import Flask, jsonify, request
from functools import wraps
import jwt
from math import sqrt
from auths.routes import auth_bp
from jogadores.routes import jogadores_bp
import config

DB_CONFIG = config.DB_CONFIG

app = Flask(__name__)
app.register_blueprint(jogadores_bp)
app.register_blueprint(auth_bp)




if __name__ == "__main__":
    app.run(host="localhost",port ="5000",debug=True)
