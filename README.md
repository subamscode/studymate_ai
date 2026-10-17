<<<<<<< HEAD
# ✦ StudyMate AI — Your Personal AI Study Partner

**StudyMate AI** is an AI-powered learning assistant built to help students understand concepts, practice programming, and learn from their own study materials. Developed using Python and Django, it combines conversational AI with Retrieval-Augmented Generation (RAG) to answer questions using uploaded documents.

🔗 **GitHub Repository:** [https://github.com/subamscode/studymate_ai](https://github.com/subamscode/studymate_ai)

## 🚀 Features

- 🤖 **AI Chat Assistant** — Ask questions and explore concepts through conversational AI.
- 📚 **Document-Based Learning** — Upload PDF and TXT notes and ask questions about their content.
- 🧠 **Retrieval-Augmented Generation (RAG)** — Retrieve relevant document passages to support context-aware answers.
- 💻 **Local AI with Ollama** — Run a compatible language model locally.
- 🔐 **User Authentication** — Register, log in, and access your personal workspace.
- 💬 **Chat History** — Continue previous conversations and start new ones.
- 📂 **Document Management** — Upload and manage your study materials.
- 📱 **Responsive UI** — A clean interface built with HTML, CSS, and JavaScript.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| SQLite3 | Relational database |
| ChromaDB | Vector storage and retrieval |
| Ollama | Local language model runtime |
| RAG | Document-grounded question answering |
| Sentence Transformers | Text embeddings |
| HTML, CSS, JavaScript | Frontend development |

## ⚙️ How It Works

1. Create an account and log in.
2. Upload study notes in PDF or TXT format.
3. The application extracts and processes document text.
4. Text embeddings are generated and stored in ChromaDB.
5. Ask a question about your study materials.
6. Relevant passages are retrieved and supplied to the configured language model to help generate an answer.

*The exact workflow depends on the implementation and configuration of the project.*

## 📋 Prerequisites

Before running the application, install:

- Python compatible with the project's dependencies
- Git
- Ollama
- A language model supported by your configuration
- pip

## 💻 Installation and Setup

### 1. Clone the repository

Open PowerShell or the VS Code terminal and run:

```powershell
git clone https://github.com/subamscode/studymate_ai.git
cd studymate_ai
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Install project dependencies

If `requirements.txt` exists in the repository:

```powershell
python -m pip install -r requirements.txt
```

### 4. Install Ollama and download a model

Install Ollama from [https://ollama.com](https://ollama.com).

If your application is configured to use Llama 3.2 (3B), run:

```powershell
ollama pull llama3.2:3b
```

Ensure Ollama is running and that the model name matches the application's configuration.

### 5. Configure environment variables

If the project uses a `.env` file, create one in the project root and add the required settings.

**Security:** Never commit passwords, secret keys, API tokens, or other sensitive credentials to GitHub.

### 6. Apply database migrations

```powershell
python manage.py migrate
```

### 7. Start the Django development server

```powershell
python manage.py runserver
```

Open the application in your browser:

**http://127.0.0.1:8000/**

## 📁 Project Structure

The following is an illustrative structure. Actual files may differ from your repository.

```text
studymate_ai/
├── manage.py
├── requirements.txt
├── assistant_app/
├── studymate/
├── templates/
│   └── assistant_app/
├── static/
│   ├── css/
│   └── js/
├── media/
├── chroma_db/
├── .gitignore
└── README.md
```

Generated databases, vector stores, uploaded files, and environment files may be created when the application runs. Keep private or sensitive data out of the public repository.

## 🎯 Use Cases

- Learn Python and other programming concepts.
- Review lecture notes and course materials.
- Ask questions about uploaded study documents.
- Summarize study material.
- Practice coding and improve problem-solving skills.

## 🔒 Security and Privacy

- Keep your Django `SECRET_KEY` private.
- Set `DEBUG = False` before production deployment.
- Configure `ALLOWED_HOSTS`, HTTPS, and secure cookies for production.
- Exclude `.env`, virtual environments, private uploads, and credentials from Git.
- Review all files before making the repository public.

## 🛣️ Future Enhancements

- Streaming AI responses
- Source references for document-based answers
- Improved PDF extraction
- Conversation search and export
- Support for additional language models
- Cloud deployment and production monitoring

## 👨‍💻 Author

**Subham Nayak**

B.Tech Computer Science and Engineering Student

Interested in Python Development, Generative AI, and Software Engineering.

## ⭐ Support

If you find this project useful, consider giving the repository a star on GitHub.

---

*StudyMate AI — Learn smarter. Understand deeper. Build with confidence.*
=======
# studymate_ai
An AI-powered study assistant that answers questions, explains coding concepts, and helps students learn from uploaded PDF and TXT notes.
>>>>>>> origin/main
