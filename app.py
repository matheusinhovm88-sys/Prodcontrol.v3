import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

# A chave NUNCA fica no código. Ela vem de uma variável de ambiente configurada
# no Vercel (Settings -> Environment Variables), com o conteúdo COMPLETO do
# arquivo JSON baixado do Firebase (Google Cloud) — sem editar nada nele.
if not firebase_admin._apps:
    chave_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
    if not chave_json:
        raise RuntimeError(
            "Variável de ambiente FIREBASE_SERVICE_ACCOUNT_JSON não encontrada. "
            "Configure no Vercel em Settings -> Environment Variables."
        )
    # Blindagem contra copiar/colar pelo celular: se sobrar algum espaço, quebra de
    # linha ou texto extra antes/depois do JSON, pegamos só o trecho entre a
    # primeira "{" e a última "}" antes de tentar interpretar.
    inicio = chave_json.find("{")
    fim = chave_json.rfind("}")
    if inicio == -1 or fim == -1 or fim < inicio:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT_JSON não parece conter um JSON válido "
            "(não encontrei '{' e '}'). Revise o valor colado no Vercel."
        )
    try:
        credenciais_dict = json.loads(chave_json[inicio:fim + 1])
    except json.JSONDecodeError as erro:
        raise RuntimeError(
            f"FIREBASE_SERVICE_ACCOUNT_JSON contém JSON inválido: {erro}. "
            "Apague o valor no Vercel e cole novamente, só uma vez, o conteúdo "
            "exato do arquivo .json baixado do Google Cloud."
        ) from erro
    cred = credentials.Certificate(credenciais_dict)
    default_app = firebase_admin.initialize_app(cred)
else:
    default_app = firebase_admin.get_app()

db = firestore.client(app=default_app)


@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})


if __name__ == '__main__':
    app.run(debug=True)