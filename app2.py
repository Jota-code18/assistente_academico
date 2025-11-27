from flask import Flask, render_template, request, jsonify  # importa Flask e utilitários para renderizar templates, ler requisições e devolver JSON
import google.generativeai as genai  # importa o SDK da API generativa do Google (Gemini)
import traceback  # importa utilitário para formatar tracebacks em caso de erro
from datetime import datetime  # importa datetime para obter a data/hora atual

app = Flask(__name__)  # cria a aplicação Flask

# Configuração da API Gemini
GEMINI_API_KEY = "AIzaSyCPjtqRJm77NN7twn_t8Mn3eYYBeJXb0xQ"  # chave de API (***evite deixar hardcoded em produção***)
genai.configure(api_key=GEMINI_API_KEY)  # configura o cliente genai com a chave informada

# Modelo
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')  # instancia o modelo generativo específico a ser usado
print("✓ Modelo configurado com sucesso.")  # imprime no console que a configuração do modelo foi realizada

# Carregamento da base local
try:
    with open("dados_academicos.txt", "r", encoding="utf-8") as f:  # tenta abrir o arquivo local com dados acadêmicos
        texto_completo = f.read()  # lê todo o conteúdo do arquivo para uma string
    dados_base = [p.strip() for p in texto_completo.split("\n\n") if p.strip()]  # separa por blocos (dupla quebra de linha) e limpa espaços
except FileNotFoundError:
    dados_base = ["Base de dados não encontrada."]  # se o arquivo não existir, usa mensagem substituta na base de dados

# Função para gerar o prompt dinâmico (com data atual)
def gerar_prompt_sistema():
    data_hoje = datetime.now().strftime("%d/%m/%Y (%A)")  # formata a data atual em dia/mês/ano (e dia da semana)
    return (
        f"Hoje é {data_hoje}. Você é um assistente acadêmico da UniEVANGÉLICA. "
        "Responda de forma clara, curta e direta (máximo 4-5 linhas). "
        "Use português formal e simples. "
        "Se não souber, diga 'Poxa, não tenho essa informação disponível!! Mas posso continuar te ajudando com outros assuntos, como seu calendário de aulas, notas das avaliações entre outros.'.\n\n"
        f"--- BASE DE DADOS ---\n{' '.join(dados_base)}\n--- FIM ---"
    )  # monta e retorna o prompt de sistema que inclui data, instruções de estilo e a base de dados carregada

# Função de resposta
def responder_avancado(pergunta):
    try:
        sistema_prompt = gerar_prompt_sistema()  # gera o prompt de sistema atualizado (com data e base)
        mensagem = f"{sistema_prompt}\n\nPergunta do usuário: {pergunta}"  # concatena o prompt do sistema com a pergunta do usuário
        response = model.generate_content(mensagem)  # envia a mensagem ao modelo e captura a resposta gerada
        resposta = response.text.strip()  # extrai o texto da resposta e remove espaços em branco nas extremidades
        return resposta  # retorna a resposta pronta
    except Exception as e:
        print(traceback.format_exc())  # em caso de erro, imprime o traceback completo no console para depuração
        return f"Erro ao processar: {str(e)}"  # retorna uma mensagem curta com o erro ocorrido

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')  # renderiza e retorna o arquivo HTML 'index.html' quando a raiz for acessada

# Rota de API para responder perguntas
@app.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.get_json()  # obtém o JSON enviado na requisição POST
    pergunta = data.get("pergunta", "")  # extrai o campo 'pergunta' do JSON, padrão para string vazia se não existir
    if not pergunta.strip():  # valida se a pergunta não é vazia (após remover espaços)
        return jsonify({"resposta": "Pergunta vazia."})  # retorna JSON com mensagem de erro simples
    resposta = responder_avancado(pergunta)  # chama a função que consulta o modelo e obtém a resposta
    return jsonify({"resposta": resposta})  # retorna a resposta em formato JSON

if __name__ == '__main__':
    app.run(debug=True)  # inicia o servidor Flask em modo debug


