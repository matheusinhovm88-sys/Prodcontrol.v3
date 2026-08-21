import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore

app = Flask(__name__)
CORS(app)

# Pega o texto da Vercel e corrige quebras de linha caso o painel tenha alterado
raw_key = os.environ.get('FIREBASE_CREDENTIALS')
if raw_key:
    # Remove aspas extras se houver e conserta o formato JSON
    raw_key = raw_key.strip()
    if raw_key.startswith('"') and raw_key.endswith('"'):
        raw_key = raw_key[1:-1]
    
    # Converte para dicionário de forma segura
    key_dict = json.loads(raw_key.replace('\\\\n', '\\n'))
    cred = credentials.Certificate(key_dict)
    initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})

if __name__ == '__main__':
    app.run(debug=True)