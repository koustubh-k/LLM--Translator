# streamlit_app.py
import streamlit as st
import requests # Used to make HTTP requests to the LangServe backend

# Define the URL of your LangServe endpoint
# Make sure this matches the host and port your server.py is running on
LANGSERVE_URL = "http://localhost:8000/chain/invoke"

st.set_page_config(page_title="LLM Translator", layout="centered")

st.title("🌐 LLM Translator with Groq (via LangServe)")
st.markdown("Enter text and choose a target language for translation.")

# Input fields for the user
input_text = st.text_area("Enter text to translate:", height=150)
target_language = st.text_input("Target Language (e.g., French, Spanish, German):", "French")

# Button to trigger translation
if st.button("Translate"):
    if input_text and target_language:
        with st.spinner(f"Translating to {target_language}..."):
            try:
                # Prepare the payload for the LangServe endpoint
                # This must match the input variables expected by your Langchain chain
                payload = {
                    "input": {
                        "language": target_language,
                        "input_text": input_text
                    }
                }

                # Send POST request to the LangServe endpoint
                response = requests.post(LANGSERVE_URL, json=payload)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

                # LangServe's /invoke endpoint returns a JSON with 'output' key
                # The output from StrOutputParser will be directly in the 'output' field
                translated_text = response.json().get('output', 'Translation failed or no output received.')

                st.subheader("Translated Text:")
                st.success(translated_text)

            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the LangServe backend. "
                         "Please ensure 'server.py' is running at http://localhost:8000.")
            except requests.exceptions.HTTPError as e:
                st.error(f"HTTP Error during translation: {e}. Response: {response.text}")
                st.write("Please check the server logs for more details.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter both text to translate and a target language.")

st.markdown("---")
st.caption("Powered by Langchain, Groq, FastAPI, and Streamlit.")