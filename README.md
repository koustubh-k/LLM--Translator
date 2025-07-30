# LLM Translator Application

This project demonstrates a robust architecture for building AI applications, separating the LLM inference logic into a backend API and providing a user-friendly frontend.

## Components Used

This project leverages the following key technologies:

1.  **LangChain:**
    * A framework for developing applications powered by large language models (LLMs).
    * **Purpose:** Simplifies the process of designing and chaining LLM calls, managing prompts, and parsing outputs.

2.  **Groq:**
    * A company providing specialized hardware (LPUs - Language Processing Units) and an API for incredibly fast LLM inference.
    * **Purpose:** The `ChatGroq` model is used as the underlying LLM to perform the text translation with blazing speed.

3.  **FastAPI:**
    * A modern, fast (high-performance) web framework for building APIs with Python.
    * **Purpose:** Serves as the foundation for the backend server, handling HTTP requests and providing automatic API documentation (`/docs`).

4.  **LangServe:**
    * A LangChain library designed to easily deploy LangChain runnables and chains as REST APIs.
    * **Purpose:** Seamlessly integrates with FastAPI to expose the Langchain translation chain as an API endpoint, complete with a built-in playground (`/chain/playground`).

5.  **Streamlit:**
    * An open-source Python framework for turning data scripts into shareable web apps.
    * **Purpose:** Provides the interactive and user-friendly frontend for the application, allowing users to input text and display translated output. It sends requests to the LangServe backend.

6.  **`python-dotenv`:**
    * A Python library to read key-value pairs from a `.env` file and set them as environment variables.
    * **Purpose:** Securely manages API keys (like `GROQ_API_KEY`) and other sensitive configurations, keeping them out of the main codebase.

## How They Work Together

* The **`server.py`** file (running on FastAPI and LangServe) acts as the **backend**. It initializes the `ChatGroq` LLM via Langchain and defines a translation `chain`. LangServe then automatically creates an API endpoint (`/chain/invoke`) that exposes this translation functionality.
* The **`streamlit_app.py`** file acts as the **frontend**. It provides text input fields and a button. When the user interacts with it, Streamlit sends an HTTP POST request to the `/chain/invoke` endpoint of the running `server.py` application.
* The `server.py` receives the request, passes the input to the Langchain `chain` (which uses the Groq model), gets the translated response, and sends it back to the `streamlit_app.py`.
* Finally, the `streamlit_app.py` receives and displays the translated text to the user.
* `python-dotenv` ensures that sensitive API keys are loaded securely for the backend.

This architecture effectively separates the UI logic from the core LLM inference logic, making the application modular, scalable, and easier to maintain.
