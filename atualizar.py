import time
import os
import pandas as pd
import mysql.connector
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurações do Banco de Dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "prodcontrol"

def processar_planilha(caminho_arquivo):
    print(f"\n[🕒] Novo arquivo detectado: {os.path.basename(caminho_arquivo)}")
    print("Processando dados, aguarde...")
    
    try:
        # Aguarda 1 segundo para garantir que o arquivo terminou de ser copiado/salvo na pasta
        time.sleep(1)
        
        # Lê a aba 'ORDENS' da planilha
        df = pd.read_excel(caminho_arquivo, sheet_name='ORDENS')
        print(f"-> Lidos {len(df)} registros da planilha.")
        
        # Conecta ao banco de dados MySQL
        conexao = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conexao.cursor()
        
        # Comando SQL para inserir os dados
        sql = """
            INSERT INTO ordens_producao (lote, ordem, qtde, cod_item, descricao, unidade, mascara) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        contador = 0
        for _, linha in df.iterrows():
            valores = (
                str(linha['Lote']),
                str(linha['Ordem']),
                float(linha['Qtde.']) if pd.notna(linha['Qtde.']) else 0.0,
                str(linha['Cód. Item']),
                str(linha[' Descrição']) if pd.notna(linha[' Descrição']) else '',
                str(linha['Unidade']) if pd.notna(linha['Unidade']) else '',
                str(linha['Máscara']) if pd.notna(linha['Máscara']) else ''
            )
            cursor.execute(sql, valores)
            contador += 1

        conexao.commit()
        print(f"[✅] Sucesso! {contador} registros inseridos no banco de dados automaticamente.")
        
    except Exception as e:
        print(f"[❌] Erro ao processar o arquivo: {e}")
        if 'conexao' in locals() and conexao.is_connected():
            conexao.rollback()
            
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

class MonitorPasta(FileSystemEventHandler):
    def on_created(self, event):
        # Se um arquivo novo for criado/jogado na pasta e terminar com .xlsx
        if not event.is_directory and event.src_path.endswith('.xlsx'):
            processar_planilha(event.src_path)

if __name__ == "__main__":
    pasta_para_observar = "." # Vigia a pasta atual onde o script está
    
    event_handler = MonitorPasta()
    observer = Observer()
    observer.schedule(event_handler, path=pasta_para_observar, recursive=False)
    
    observer.start()
    print("==================================================")
    print("👁️  Sistema de monitoramento automático ligado!")
    print("Deixe esta janela aberta. Sempre que você jogar")
    print("uma planilha .xlsx aqui, ela será lida sozinha.")
    print("==================================================")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()