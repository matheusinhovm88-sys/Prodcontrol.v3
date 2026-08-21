import os
from flask import Flask, jsonify
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore

app = Flask(__name__)
CORS(app)

# Carrega o arquivo JSON de forma segura usando o caminho absoluto da pasta atual
caminho_chave = os.path.join(os.path.dirname(__file__), "chave.json")
cred = credentials.Certificate(caminho_chave)
initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})

if __name__ == '__main__':
    app.run(debug=True)