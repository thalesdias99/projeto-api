import requests

def test_busca_cep():
    response = requests.get("https://viacep.com.br/ws/01001000/json/")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert "logradouro" in data
    assert data["localidade"] == "São Paulo"