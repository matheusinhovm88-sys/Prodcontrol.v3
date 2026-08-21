import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, firestore

app = Flask(__name__)
CORS(app)

# Lê a chave diretamente da variável de ambiente da Vercel
firebase_key = json.loads(os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON'))
cred = credentials.Certificate(firebase_key)
initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)