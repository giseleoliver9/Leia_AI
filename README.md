# Leia.ai 📚

Recomendador literário inteligente desenvolvido com **Python**, **Streamlit** e a API de alta velocidade do **Groq** (usando o modelo Llama 3.3).

O **Leia.ai** une a precisão de um catálogo local de livros (com mais de 10.000 títulos do dataset GoodBooks-10K) com o poder criativo e analítico de um Large Language Model (LLM) para entregar sugestões literárias ricas, personalizadas e explicadas em linguagem natural.

---

## ✨ Funcionalidades Principais

* **Busca Híbrida Inteligente**: Prioriza e busca livros diretamente do catálogo local (`books.csv`) e, caso necessário, complementa com o vasto conhecimento literário global da IA.
* **Chips e Histórico Interativos**: Facilita a navegação do usuário através de chips de atalho de gêneros e um histórico de pesquisa na barra lateral que preenchem o prompt automaticamente ao serem clicados.
* **Capas Reais e Dinâmicas**: Exibe a capa oficial do livro (via Goodreads ou Open Library). Se o livro não possuir imagem cadastrada ou ocorrer falha de rede, um fallback baseado no hash do título gera uma capa abstrata em gradiente elegante.
* **Links de Atalho Úteis**: Atalhos integrados para pesquisar o livro recomendado no **Goodreads** ou no **Google Books** com um único clique.
* **Design Premium e Responsivo**: Visual minimalista e escuro com efeitos de vidro (glassmorphism), micro-animações de aproximação nas capas e comportamento responsivo de tela.

---

## 🛠️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:
* **Python 3.8** ou superior
* Gerenciador de pacotes **pip**

---

## 📦 Instalação

1. Clone o repositório do GitHub:
   ```bash
   git clone https://github.com/giseleoliver9/Leia_AI.git
   ```
2. Acesse a pasta do projeto pelo terminal:
   ```bash
   cd Leia_AI
   ```
3. Instale as dependências necessárias utilizando o arquivo de requisitos:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuração de Credenciais

O projeto utiliza o arquivo `.env` para armazenar de forma segura suas chaves de API, evitando exposição pública.

1. Na raiz do projeto, crie ou edite o arquivo `.env`:
   ```env
   GROQ_API_KEY=sua_chave_api_do_groq_aqui
   ```
2. *(Opcional)* Certifique-se de obter uma chave gratuita registrando-se no painel da [Groq Console](https://console.groq.com/).

---

## 🚀 Como Executar

Inicie a aplicação local do Streamlit executando o comando abaixo no terminal:

```bash
streamlit run leia_ai.py
```

O aplicativo abrirá automaticamente no seu navegador padrão no endereço local **http://localhost:8501**.

---

## 📂 Estrutura de Arquivos

```
leia-ai/
├── archive/
│   └── books.csv                 # Dataset do catálogo local (GoodBooks-10K)
├── .env                          # Chave da API do Groq (ignorado pelo git)
├── .gitignore                    # Regras de exclusão de arquivos no Git
├── leia_ai.py                    # Script principal da aplicação Streamlit
├── logo.jpg                      # Identidade visual da barra lateral
├── README.md                     # Documento de apresentação do projeto (Este arquivo)
└── TECHNICAL_DOCUMENTATION.md    # Documentação de arquitetura e código do app
```
