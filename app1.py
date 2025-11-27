from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import traceback
import os

app = Flask(__name__)

# =======================
# CONFIGURAÇÃO DO GEMINI
# =======================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCPjtqRJm77NN7twn_t8Mn3eYYBeJXb0xQ")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
print("✓ Modelo configurado: gemini-2.5-flash-preview-05-20")

# =======================
# CARREGAR BASE DE DADOS
# =======================
try:
    with open("dados_academicos.txt", "r", encoding="utf-8") as f:
        texto_completo = f.read()

    dados_base = [p.strip() for p in texto_completo.split("\n\n") if p.strip()]
    total = sum(len(p) for p in dados_base)

    if total > 30000:
        print(f"⚠ Base muito grande ({total} chars), reduzindo...")
        nova = []
        atual = 0
        for p in dados_base:
            if atual + len(p) < 30000:
                nova.append(p)
                atual += len(p)
            else:
                break
        dados_base = nova
        print(f"✓ Base reduzida ({atual} chars)")
    else:
        print(f"✓ Base carregada ({total} chars)")

except FileNotFoundError:
    print("⚠ Arquivo 'dados_academicos.txt' não encontrado.")
    dados_base = ["Nenhum dado disponível no momento."]

# =======================
# CONFIGURAÇÃO DO PROMPT
# =======================
sistema_prompt = (
    "Você é um assistente acadêmico da UniEVANGÉLICA. "
    "Seja DIRETO e OBJETIVO nas respostas. "
    "Responda em no máximo 4-5 linhas, com parágrafos simples e sem listas. "
    "Use as informações fornecidas abaixo. "
    "Se não souber a resposta com base nesses dados, diga: "
    "'Poxa, não tenho essa informação disponível!! Mas posso continuar te ajudando com outros assuntos, como seu calendário de aulas e vários outros assuntos.'\n\n"
    f"--- BASE DE DADOS ---\n{' '.join(dados_base)}\n--- FIM DA BASE ---"
)

historico_chat = []

# =======================
# FUNÇÃO DE RESPOSTA
# =======================
def responder_avancado(pergunta):
    try:
        print(f"\n📨 Pergunta: {pergunta[:100]}")

        mensagem = f"{sistema_prompt}\n\nPergunta do usuário: {pergunta}"

        if len(mensagem) > 100000:
            return "Desculpe, a base está muito grande. Contate o administrador."

        response = model.generate_content(mensagem)
        resposta = response.text.strip()
        historico_chat.append({"usuario": pergunta, "assistente": resposta})
        return resposta

    except Exception as e:
        print("❌ ERRO:", traceback.format_exc())
        return "Erro ao processar a pergunta."


# =======================
# ROTAS DO SITE
# =======================

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/assistente', methods=['GET', 'POST'])
def assistente():
    resposta = ""
    pergunta = ""
    if request.method == 'POST':
        pergunta = request.form.get('mensagem', '').strip()
        if pergunta:
            resposta = responder_avancado(pergunta)

    return render_template('assistente.html', pergunta=pergunta, resposta=resposta)


# =======================
# EXECUÇÃO
# =======================
if __name__ == '__main__':
    app.run(debug=True)
