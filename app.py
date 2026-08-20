import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore, storage

app = Flask(__name__)
CORS(app)

# Inicialização inteligente do Firebase (Funciona na Vercel e Local)
if 'FIREBASE_SERVICE_ACCOUNT_JSON' in os.environ:
    # Se estiver na Vercel, pega da variável de ambiente
    key_dict = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'))
    cred = credentials.Certificate(key_dict)
else:
    # Se estiver rodando no seu computador localmente, usa o arquivo chave.json
    cred = credentials.Certificate("chave.json")

initialize_app(cred)
db = firestore.client()

# Suas rotas e o restante do seu código continuam aqui abaixo
@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)