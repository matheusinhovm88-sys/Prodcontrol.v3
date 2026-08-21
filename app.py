from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

app = Flask(__name__)
CORS(app)

# Chave dividida em linhas puras em formato de lista para evitar qualquer erro de barra invertida
private_key_lines = [
    "-----BEGIN PRIVATE KEY-----",
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCkpASYMwnDvP/w",
    "Ri4EublSixMjlfi50KTZ0opNFUHCy3/86Cn1SEoJBxaxExmtF8WRv5xgz/H/L3Ht",
    "rRPcdWyp5EZ8KAX4xDubRHbmNSV7w1oZ0EHsG1dd67Ks1NkUuBcI28eWeX12mk+r",
    "DqEexXjWIDEAkhwyLJuzP3cl7jh1/bANdmwn7uc5VO8RmrnxBBj2AnF98TiFl097",
    "2puva4dgCY/Z3EDU2zQzOh7bwvNgHn7YznzaZSQWFMKxRL5p9NZQctJU9kqBmF3/",
    "v0yqg4ZGO9MSnMMwTiRgfXWnEfU24BelHpNO+weYJ8ws9sRTuXKtGfsNcyxvZf/F",
    "3YqO6hYtAgMBAAECggEACTjixP++4Ub58ySLOVqJ5fTCWrDw4L+uLEFd29l/+IBb",
    "p/f9Oa8V7pGGFN8kBg0Z1QMtqEKdpJSsxgp23Vd6gb22sQew5fFgAV+BZX2+nsMf",
    "jeibeLVDXJByTroRetag+68L7ALcI0ObiNJl9gpLrXraI9ULXUggZJb+fpJseTdo",
    "lKtsAIueORefAVdtYSQKqOP23VSvMXiI5Zau+4ZG7FeXX6IhceTaxmNFsc0TPC4B",
    "BS0ySfyGkyvI75Sqs/NCjBrYsqEnr9QAdultcFRF/SoqN7HhgoW2JBYid7XBkbJx",
    "00YgM8vHhbqsmmIXaPgkAtNaGGrNHuay44/gvB3hBQKBgQDakfhW3iLUsf86hZRZ",
    "iZ78Ze2jejG3y/6kmKTE5XZkd7/vhojGoNuxDAGWeq3HmKUcUhRDeyTU8CCenI/H",
    "5ub5az0ndNpR1QbCCG3y1FvqBNC12E4TmLhp9HvosMTdanaqVnSvmifpTVmifbuB",
    "eS3vhiTXSx9iB0AT6FOWMIZcbwKBgQDA1czWdWiTWc7mM5HeGQ1l3B6Vt6DIVTIh",
    "XClRBWyQACvMl4/uzLLTeM7ycTUtXYdjR+FiFcM72kPpRKSf/x3eDi/SzQMNvEfy",
    "p1agWzsLYkDT4CHU32W0KOap6c2G2yAHTbDUcI387Ey1x5cv83jTElw289jPGZGJ",
    "zHhKbEs9IwKBgQCR5wcD1d0iZn+drTXOX1PF4LS1gAhYTNB7R3oWBab2ggmZ9xCu",
    "wqAMSeOL+55Yqg1M4VbVoTLsE/WEWTZaIWe0btM73AdWDreo4nho2iH2xcHjJDx",
    "++x+rjlYp0eDFmKIapYR8rHZx0yib5QPZbkIP1+wZ/FXGsfnghrqExJd+QKBgHtz",
    "ZGOXXo+W2yH8udGZ8D3Zoarvl/sor6MzwS+hbVLzCRc9oGOcoI9JtBL57rVQPzCL",
    "//ovPIHAxeE8lLfpN1HFe1BU9zN/6f+qqYaXYUF0cVQzFPWW3yFrXeBBUdaXyfVj",
    "A2W9eOkGzkVBtcR49k0KYAa+LXrIP6gcQpZCphhJAoGAXxzaqI0pGhUJ7TQmIBBj",
    "nzFgG7PNzS3vNQ3Wf50Ao1DZMzf4/iZebI3u4jaZDgC6wvqIUd/Sy+mcHu1uds2ZK",
    "XWXfAQmEzzNMTpQUo2y/OPr/mzuI9ikHIX84OW/VCCtWiwIjquqzRTYOsj9bXKRp",
    "Svyn9dKQLvS/MK4I0jROprE=",
    "-----END PRIVATE KEY-----"
]

firebase_config = {
  "type": "service_account",
  "project_id": "teste-do-prodcontrol-of",
  "private_key_id": "631cbf33130a09f54ac9f392a61d59941fb70e67",
  "private_key": "\n".join(private_key_lines),
  "client_email": "firebase-adminsdk-fbsvc@teste-do-prodcontrol-of.iam.gserviceaccount.com",
  "client_id": "111334111507363775759",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40teste-do-prodcontrol-of.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    default_app = initialize_app(cred)
else:
    default_app = firebase_admin.get_app()

db = firestore.client(app=default_app)

@app.route('/')
def home():
    return jsonify({"status": "API rodando com sucesso e conectada ao Firebase!"})

if __name__ == '__main__':
    app.run(debug=True)