# 🧠 Mental Health Chatbot: LangChain + Streamlit

An **AI-powered mental health support chatbot** designed to provide empathetic conversation, coping strategies, and relevant resources to users. This project leverages the power of **LangChain** for robust natural language processing and **Streamlit** for an accessible, interactive web interface, all powered by a local large language model, **Llama2 via Ollama**.

---

## ✨ Features

* **Empathetic Conversation:** Utilizes a carefully crafted system prompt to ensure responses are non-judgmental, empathetic, and supportive, mimicking a therapeutic communication style.
* **LangChain Integration:** Leverages **LangChain** to seamlessly build the conversational chain, managing the prompt template, LLM invocation, and output parsing.
* **Crisis Detection:** Implements **robust keyword detection** for signs of self-harm or suicidal ideation, providing immediate safety guidance and crisis resources as a primary response.
* **Intuitive UI with Streamlit:** Offers a friendly, interactive user interface built with **Streamlit**, making the chatbot easy to use and accessible.
* **History Management:** Maintains a truncated conversation history to keep responses contextually relevant while avoiding token limit issues.
* **Open-Source LLM:** Uses **Llama2** via **Ollama**, allowing the chatbot to run on local or private infrastructure.

---

## 🛠️ Technologies Used

* **Python**
* **LangChain:** For building the application logic and connecting components.
* **Streamlit:** For creating the interactive web application interface.
* **Ollama (Llama2):** The backend large language model providing the conversational intelligence.
* **`python-dotenv`:** For managing environment variables (API keys, settings).

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

You'll need **Python 3.8+** installed.

* **Install Ollama and Llama2:**
    * Download and install [**Ollama**](https://ollama.com/).
    * Run the following command in your terminal to pull the Llama2 model:
        ```bash
        ollama pull llama2
        ```
    * Ensure the Ollama server is running (usually started automatically or by running `ollama serve`).

### 2. Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-link>
    cd <project-directory>
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate   # On Windows
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    **(Content of `requirements.txt`):**

    ```
    streamlit
    langchain
    langchain-core
    langchain-community
    python-dotenv
    ```

### 3. Configuration

1.  **Create a `.env` file** in the project root directory.

2.  **Set the Ollama Base URL.** If Ollama is running on the default host and port, use:
    ```env
    # .env file content
    OLLAMA_BASE_URL="http://localhost:11434"

    # Optional: Set these to empty strings if not using LangSmith or OpenAI
    LANGCHAIN_TRACING_V2="false"
    LANGCHAIN_API_KEY=""
    OPENAI_API_KEY=""
    ```
    Ensure the `OLLAMA_BASE_URL` matches your running Ollama instance.

### 4. Run the Chatbot

Execute the Streamlit application from your terminal:

```bash
streamlit run <your_script_name>.py
