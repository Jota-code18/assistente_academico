UN!A – Assistente Acadêmico

O UN!A é um assistente acadêmico desenvolvido como Projeto Semestral do 1º Período do curso de Inteligência Artificial.
Seu objetivo é centralizar e facilitar a rotina universitária, reunindo em um só aplicativo tarefas, horários, notas, lembretes e informações acadêmicas.

Funcionalidades

Chatbot que auxilia na vida acadêmica
Interface intuitiva e amigável
Persistência de dados
API (back-end) integrada ao banco de dados

Tecnologias Utilizadas

Back-end:

Python
Flask 

Front-end:

HTML
CSS
JavaScript
Figma (prototipação)

 Arquitetura do Sistema

 Front-end  →  Back-end (Flask)  →  Banco de Dados (.txt)

O Front-end envia dados e solicitações pela interface.
O Back-end processa requisições, valida informações e acessa o banco.
O Banco de Dados guarda tarefas, disciplinas, usuários e notas.

Equipe de Desenvolvimento

| Nome                      | Função                |
| **JOÃO PEDRO PROPÉRCIO**  | Documentação e Gestão |
| **JOÃO VICTOR DOMINGUES** | Back-end              |
| **NICOLAS BARCELOS**      | Back-end              |
| **TALES FERREIRA**        | Banco de Dados        |
| **YOUSSEF PORTO**         | Banco de Dados        |
| **JOÃO GABRIEL NERES**    | Banco de Dados        |
| **JOÃO VITOR FREITAS**    | Front-end             |

Estrutura do Repositório

assistente-academico/
│── static/ # Arquivos estáticos (CSS, JS)
│── templates/ # Arquivos HTML de interface
│── app.py # Código-fonte principal da aplicação Flask
│── dados_academicos.txt # Arquivo de persistência de dados simples
│── requirements.txt # Lista de dependências Python
│── README.md # Este arquivo

## Como Rodar o Projeto Localmente

Siga o passo a passo abaixo para executar o UN!A – Assistente Acadêmico no seu computador.

1) Baixe o projeto:
   - Acesse o repositório: https://github.com/NicolasReis-dev/assistente-academico
   - Clique no botão "Code" (verde)
   - Selecione "Download ZIP"
   - Extraia o arquivo ZIP em uma pasta do seu computador

2) Verifique o Python instalado:
   python --version

3) Instale as dependências necessárias:
   pip install python-dotenv
   pip install google-generativeai
   pip install flask

4) Execute a aplicação:
   python app.py
   (ou python3 app.py dependendo da sua instalação)

5) Acesse no navegador:
   http://127.0.0.1:500

Pronto! O UN!A estará rodando localmente no seu navegador.

