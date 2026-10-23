# Testes da API de CEP.
#
# POR QUE MUDAR O TESTE ANTIGO?
# O teste anterior chamava o ViaCEP diretamente (requests.get("https://viacep...")).
# Isso testa o serviço DE OUTRA PESSOA, não o SEU código. Se você quebrasse a sua
# rota /cep, o teste antigo continuaria passando.
#
# Aqui fazemos duas coisas:
# 1) Usamos o "test client" do Flask, que simula requisições HTTP para o SEU app
#    sem precisar subir o servidor.
# 2) Usamos o "monkeypatch" do pytest para trocar a função buscar_cep por uma
#    versão falsa (um "mock"). Assim o teste NÃO depende da internet nem do ViaCEP
#    estar no ar: ele fica rápido e sempre dá o mesmo resultado.

import app as modulo_app  # importamos o módulo inteiro para poder trocar funções dele


def criar_cliente():
    # O test_client() cria um "navegador falso" que faz requisições ao app.
    modulo_app.app.config["TESTING"] = True
    return modulo_app.app.test_client()


def test_home_responde():
    # A rota principal "/" deve responder com status 200 (OK).
    resposta = criar_cliente().get("/")
    assert resposta.status_code == 200


def test_cep_valido_retorna_endereco(monkeypatch):
    # Resposta falsa, no mesmo formato que o ViaCEP devolveria.
    def buscar_cep_falso(cep):
        return {"logradouro": "Praça da Sé", "localidade": "São Paulo", "uf": "SP"}

    # Trocamos a função real pela falsa só durante este teste.
    monkeypatch.setattr(modulo_app, "buscar_cep", buscar_cep_falso)

    resposta = criar_cliente().get("/cep/01001000")

    assert resposta.status_code == 200
    dados = resposta.get_json()
    # Conferimos se a SUA rota traduziu os campos corretamente
    # (localidade -> cidade, uf -> estado).
    assert dados == {"logradouro": "Praça da Sé", "cidade": "São Paulo", "estado": "SP"}


def test_cep_inexistente_retorna_400(monkeypatch):
    # O ViaCEP responde {"erro": true} quando o CEP não existe.
    monkeypatch.setattr(modulo_app, "buscar_cep", lambda cep: {"erro": True})

    resposta = criar_cliente().get("/cep/00000000")

    assert resposta.status_code == 400
    assert "erro" in resposta.get_json()


def test_falha_na_api_externa_retorna_400(monkeypatch):
    # Se o ViaCEP estiver fora do ar, buscar_cep devolve None.
    monkeypatch.setattr(modulo_app, "buscar_cep", lambda cep: None)

    resposta = criar_cliente().get("/cep/01001000")

    assert resposta.status_code == 400
