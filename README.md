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

### 1. Python

Python **3.14.6**

Check your version:

```bash
python --version
```

### 2. Conda

Conda is used to create an isolated Python environment for the project.

Create the environment:

```bash
conda create -n rag-system python=3.14.6
```

Activate it:

```bash
conda activate rag-system
```

You should see:

```text
(rag-system)
```

at the beginning of your terminal.

### 3. Git

Git is required for version control.

Check your installation:

```bash
git --version
```

### 4. FastAPI

The backend API will be built using FastAPI.

It will be installed inside the `rag-system` environment.

### 5. Uvicorn

Uvicorn will be used as the ASGI server to run the FastAPI application.

It will also be installed inside the project environment.

---

## Project Setup

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project:

```bash
cd RAG-system
```

Activate the Conda environment:

```bash
conda activate rag-system
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

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

More dependencies will be added as the RAG system evolves.
