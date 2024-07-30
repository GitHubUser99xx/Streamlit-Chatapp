# Streamlit Chat Application

This is a simple chat application built using Streamlit, Langchain, and Ollama. The primary purpose of this project is to serve as a template or guide for building more advanced and complex applications in the future.

## Libraries Used

- **Streamlit**: `1.37.0`
- **Langchain**: `0.2.11`
- **Langchain-Community**: `0.2.10`

## Getting Started

Follow the instructions below to set up and run the application.

### Prerequisites

- Python 3.10 or above

### Installation

1. Clone the Repository

```bash
$ git clone https://github.com/arnabd64/Streamlit-Chatapp.git
$ cd Streamlit-Chatapp
```

2. Create a python virtual environment

```bash
$ python -m venv .venv
$ source .venv/bin/activate
```

3. Install dependencies

```bash
$ python -m pip install -r requirements.txt
```

4. Run the app

```bash
$ streamlit run app.py --server.address 127.0.0.1 --server.port 8000
```

This will start the application on `http://127.0.0.1:8000/`