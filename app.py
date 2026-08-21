from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import initialize_app, firestore

app = Flask(__name__)
CORS(app)

# Inicialização sem precisar da chave privada corrompida na Vercel
if not firebase_admin._apps:
    initialize_app(options={
        'projectId': 'teste-do-prodcontrol-of',
    })

db = firestore.client()

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})

if __name__ == '__main__':
    app.run(debug=True)