import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Inicializa o Firebase de forma segura
if not firebase_admin._apps:
    if 'FIREBASE_CONFIG' in os.environ:
        key_dict = json.loads(os.environ.get('FIREBASE_CONFIG'))
        cred = credentials.Certificate(key_dict)
    else:
        cred = credentials.Certificate("chave.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def importar_excel_para_firebase(caminho_arquivo):
    print(f"Lendo o arquivo: {caminho_arquivo}...")
    
    # Lê a planilha do Excel usando o Pandas
    df = pd.read_excel(caminho_arquivo)
    
    # Percorre cada linha da planilha e envia para o Firestore
    for index, row in df.iterrows():
        dados_linha = row.to_dict()
        id_documento = f"item_{index}"
        
        # Salva na coleção 'ordens_producao'
        db.collection('ordens_producao').document(id_documento).set(dados_linha)
        print(f"Enviado para o Firebase: {id_documento}")

    print("Importação concluída com sucesso!")

if __name__ == '__main__':
    # Usa o arquivo de ordens que está na sua pasta
    importar_excel_para_firebase('ordens.xlsx')