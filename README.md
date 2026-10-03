#  RAG App

A simple **Retrieval-Augmented Generation (RAG)** application built with **Python** and **FastAPI**.

The goal of this project is to understand how a RAG system works from end to end:

```text
User
  ↓
FastAPI
  ↓
Document Retrieval
  ↓
Relevant Context
  ↓
LLM
  ↓
Answer
```

## Requirements

Before running the project, make sure you have the following installed:

* Python **3.14.6**
* Conda
* Git

Check your installations:

```bash
python --version
conda --version
git --version
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd RAG-system
```

### 2. Create the Conda environment

Create an isolated Python environment for the project:

```bash
conda create -n rag-system python=3.14.6
```

Activate the environment:

```bash
conda activate rag-system
```

You should see:

```text
(rag-system)
```

at the beginning of your terminal.

Verify the Python version:

```bash
python --version
```

Expected:

```text
Python 3.14.6
```

---

### 3. Install dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

The project uses environment variables for configuration and sensitive values.

Create your local `.env` file from the example:

#### Git Bash / Linux / macOS

```bash
cp .env.example .env
```

#### Windows CMD

```cmd
copy .env.example .env
```

#### PowerShell

```powershell
Copy-Item .env.example .env
```

Then open the `.env` file:

```text
.env
```

and configure the required environment variables according to your local environment.

Example:

```env
APP_ENV=development

# Add your RAG / LLM configuration here
# API_KEY=
# MODEL_NAME=
# DATABASE_URL=
```

> **Important:** Never commit the `.env` file to Git.
> The `.env` file may contain secrets such as API keys and database credentials.

The `.env.example` file should contain only the required variable names and safe example values.

---

## Running the Application

Make sure the Conda environment is active:

```bash
conda activate rag-system
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

## Project Goal

This project is mainly for learning and understanding the core concepts behind RAG systems.

The main concepts we will cover are:

* Document loading
* Text splitting / chunking
* Embeddings
* Vector databases
* Similarity search
* Retrieval
* LLM integration
* Prompt construction
* FastAPI APIs
* RAG pipeline

## Development Environment

```text
Python 3.14.6
FastAPI
Uvicorn
Conda
```

More dependencies and environment variables will be added as the RAG system evolves.
