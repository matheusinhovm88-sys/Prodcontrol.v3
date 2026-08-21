import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore

app = Flask(__name__)
CORS(app)

# Recupera a variável e trata quebras de linha e aspas de forma segura
raw_key = os.environ.get('FIREBASE_CREDENTIALS')
if raw_key:
    raw_key = raw_key.strip()
    if raw_key.startswith('"') and raw_key.endswith('"'):
        raw_key = raw_key[1:-1]
    
    # Corrige barras invertidas e converte para dicionário
    try:
        key_dict = json.loads(raw_key)
    except json.JSONDecodeError:
        # Fallback caso a Vercel escape as quebras de linha
        fixed_key = raw_key.replace('\\\\n', '\\n')
        key_dict = json.loads(fixed_key)

    cred = credentials.Certificate(key_dict)
    initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})

if __name__ == '__main__':
    app.run(debug=True)