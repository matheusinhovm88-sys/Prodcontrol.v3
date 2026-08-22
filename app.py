from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore
import os
import json

app = Flask(__name__)
CORS(app)

firebase_json_str = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')

if not firebase_admin._apps:
    if firebase_json_str:
        firebase_config = json.loads(firebase_json_str)
        cred = credentials.Certificate(firebase_config)
        default_app = initialize_app(cred)
    else:
        raise ValueError("A variável de ambiente FIREBASE_SERVICE_ACCOUNT_JSON não foi configurada na Vercel!")
else:
    default_app = firebase_admin.get_app()

db = firestore.client(app=default_app)

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})

if __name__ == '__main__':
    app.run(debug=True)