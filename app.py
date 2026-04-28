from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Função para buscar dados do CEP
def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return None
        
        return response.json()
    
    except requests.RequestException:
        return None


# Rota principal (opcional)
@app.route("/")
def home():
    return "API de CEP funcionando!"


# Rota para buscar CEP
@app.route("/cep/<cep>")
def get_cep(cep):
    data = buscar_cep(cep)

    if data is None or "erro" in data:
        return jsonify({"erro": "CEP inválido ou falha na API externa"}), 400

    return jsonify({
        "logradouro": data.get("logradouro"),
        "cidade": data.get("localidade"),
        "estado": data.get("uf")
    })


# Execução (compatível com Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)