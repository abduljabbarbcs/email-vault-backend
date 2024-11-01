from functools import wraps
from flask import request, jsonify
from rococo.auth import validate_access_token
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='../.env.secrets')
env = os.environ

def auth_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        
        entity_id = validate_access_token(auth_token, env['VERIFICATION_KEY'], 3600)
        if not auth_token or not entity_id: 
            return jsonify({"error": "Unauthorized"}), 401
        kwargs['entity_id'] = entity_id
        return f(*args, **kwargs)
    return decorated_function

