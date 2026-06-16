# BotQuímica 🧪

Assistente educacional de química criado para o trabalho do **Colégio Modelo de São Sebastião**.

**Equipe:** Pedro (Au) · Murilo (Fe) · Kawan (Cu) · Augusto (O) · Pietro (Hg)

## Como rodar

### 1. Instala as dependências
```bash
pip install flask requests python-dotenv
```

### 2. Cria o arquivo `.env` na pasta do projeto
```
GROQ_API_KEY=gsk_...sua chave aqui...
```
> Chave gratuita em: https://console.groq.com

### 3. Roda o servidor
```bash
python app.py
```

### 4. Abre no navegador
```
http://localhost:5000
```

## Tecnologias
- **Backend:** Python + Flask
- **IA:** Groq API (gratuita) + LLaMA 3.1
- **Frontend:** HTML + Tailwind CSS