from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app)

# Inicialização inteligente do Firebase (funciona no PC e na Vercel)
if 'FIREBASE_CONFIG' in os.environ:
    key_dict = json.loads(os.environ.get('FIREBASE_CONFIG'))
    cred = credentials.Certificate(key_dict)
else:
    cred = credentials.Certificate("chave.json")

firebase_admin.initialize_app(cred)

# Rota 1: Ler dados do Firestore
@app.route('/api/dados', methods=['GET'])
def get_dados():
    try:
        db = firestore.client()
        doc_ref = db.collection('sistema').document('status')
        doc = doc_ref.get()
        
        if not doc.exists:
            doc_ref.set({"status": "Conectado com sucesso", "projeto": "ProdControl"})
            doc = doc_ref.get()
            
        return jsonify(doc.to_dict()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota 2: Salvar dados no Firestore
@app.route('/api/salvar', methods=['POST'])
def salvar_dado():
    try:
        db = firestore.client()
        doc_ref = db.collection('producao').document('lote_001')
        doc_ref.set({
            "pecas_produzidas": 150,
            "status": "Em andamento",
            "turno": "Manhã"
        })
        return jsonify({"mensagem": "Dado salvo com sucesso no Firebase!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)