"""
BotQuímica — Backend Flask + Groq (gratuito)
"""

import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

CONTEXTO = """Você é o BotQuímica, assistente do trabalho escolar de química do Colégio Modelo de São Sebastião.
Equipe: Pedro (Au/Ouro), Murilo (Fe/Ferro), Kawan (Cu/Cobre), Augusto (O/Oxigênio), Pietro (Hg/Mercúrio).
Responda em português, de forma simples e didática. Use **negrito** para termos importantes.

ELEMENTOS:
- Au (79): metal precioso, maleável. Usos: joalheria, eletrônica, medicina.
- Fe (26): mais abundante na crosta. Base do aço. Usos: construção, hemoglobina, indústria.
- Cu (29): excelente condutor elétrico. Usos: fios, encanamento, antimicrobial.
- O (8): 21% da atmosfera. Usos: respiração, combustão, medicina.
- Hg (80): único metal líquido. Fusão -38,83°C. Tóxico. Usos antigos: termômetros, lâmpadas.

METAIS DE TRANSIÇÃO: grupos 3-12, bloco d, subcamada d incompleta. Condutores, brilho metálico, NOX variável.

MATÉRIA: Substância Simples (1 elemento), Composta (2+ elementos), Mistura Homogênea (1 fase), Heterogênea (2+ fases)."""


def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def chamar_groq(historico):
    if not GROQ_API_KEY:
        return "Chave não configurada."

    mensagens = [{"role": "system", "content": CONTEXTO}]
    for msg in historico[-4:]:
        mensagens.append({"role": msg["role"], "content": msg["content"]})

    headers = {
        "Authorization": "Bearer " + GROQ_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": mensagens,
        "max_tokens": 400,
        "temperature": 0.7
    }

    try:
        resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        data = resp.json()
        if resp.status_code != 200:
            return "Erro da API: " + data.get("error", {}).get("message", "Desconhecido")
        return data["choices"][0]["message"]["content"]
    except requests.Timeout:
        return "Tempo limite esgotado. Tente novamente."
    except Exception as e:
        return "Erro: " + str(e)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return add_cors(jsonify({}))
    data = request.get_json(force=True)
    historico = data.get("historico", [])
    if not historico:
        return add_cors(jsonify({"erro": "Histórico vazio"})), 400
    resposta = chamar_groq(historico)
    return add_cors(jsonify({"resposta": resposta}))


@app.route("/ping")
def ping():
    return add_cors(jsonify({"status": "ok"}))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
