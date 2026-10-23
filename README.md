# CEP Lookup API 📮

A small REST API built with **Python + Flask** that returns the address for a Brazilian postal code (CEP), using the public [ViaCEP](https://viacep.com.br) API.

> 🇧🇷 API REST em Python/Flask que consulta endereços a partir do CEP.

## ✨ Features

- `GET /cep/<cep>` → returns street, city and state as JSON
- Error handling for invalid CEPs and external API failures (returns `400`)
- Automated tests with **pytest**
- Continuous integration with **GitHub Actions**
- Ready to deploy on **Render** (`render.yaml` + `Procfile`)

## 🛠️ Tech stack

Python 3.10 · Flask · Requests · Gunicorn · pytest · GitHub Actions

## 🚀 Running locally

```bash
git clone https://github.com/thalesdias99/projeto-api.git
cd projeto-api
pip install -r requirements.txt
python app.py
```

Then open: `http://localhost:5000/cep/01001000`

### Example response

```json
{
  "logradouro": "Praça da Sé",
  "cidade": "São Paulo",
  "estado": "SP"
}
```

## 🧪 Running the tests

```bash
pytest
```

## 📚 What I learned

- Building REST endpoints with Flask and returning proper HTTP status codes
- Consuming an external API safely (timeouts and exception handling)
- Setting up a CI pipeline with GitHub Actions
- Preparing an app for cloud deployment

---

Made by [Thales Freitas](https://www.linkedin.com/in/thales-freitas-64527924a)
