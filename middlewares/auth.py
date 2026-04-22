from flask import jsonify, request
from config import SECRET_KEY
import jwt
from functools import wraps
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"erro":"sem header"}),401
        auth_header_splited = auth_header.split(" ")
        if len(auth_header_splited) != 2:
            return jsonify({"erro":"header invalido"}),401
        if auth_header_splited[0] != "Bearer":
            return jsonify({"erro":"header invalido"}),401
        try:
            token = auth_header_splited[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro":"token expirado"}),401
        except jwt.InvalidTokenError:
            return jsonify({"erro":"token invalido"}),401
        except Exception:
            return jsonify({"erro":"erro interno"}),500
        if not payload.get("is_admin"):
            return jsonify({"erro":"acesso negado"}),403
        return func(*args,**kwargs)
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"erro":"sem header"}),401
        auth_header_splited = auth_header.split(" ")
        if len(auth_header_splited) != 2:
            return jsonify({"erro":"header invalido"}),401
        if auth_header_splited[0] != "Bearer":
            return jsonify({"erro":"header invalido"}),401
        try:
            token = auth_header_splited[1]
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro":"token expirado"}),401
        except jwt.InvalidTokenError:
            return jsonify({"erro":"token invalido"}),401
        except Exception:
            return jsonify({"erro":"erro interno"}),500
        return func(*args,**kwargs)


        
    return wrapper