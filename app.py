from flask import Flask, jsonify
import requests

app = Flask(__name__)

def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()

@app.route("/cep/<cep>")
def get_cep(cep):
    data = buscar_cep(cep)

    if data is None or "erro" in data:
        return jsonify({"erro": "CEP inválido"}), 400

    return jsonify({
        "logradouro": data["logradouro"],
        "cidade": data["localidade"],
        "estado": data["uf"]
    })

if __name__ == "__main__":
    app.run(debug=True)