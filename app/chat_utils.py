from euriai.langchain import create_chat_model

API_KEY = None
MODEL = "gpt-4.1-nano"
TEMPERATURE = 0.7

# This module initializes a chat model using the LangChain library.
# It provides functions to create a chat model with a specified API key, model type, and temperature setting.
## The `get_chat_model` function returns a chat model instance that can be used to interact with the language model.

def get_chat_model(api_key: str = None):
    return create_chat_model(
        api_key=api_key or API_KEY,
        model=MODEL,
        temperature=TEMPERATURE
    )

# This function sends a prompt to the chat model and returns the response content.
# It uses the `invoke` method of the chat model to get the response based on the provided prompt.
## The `ask_chat_model` function is useful for querying the chat model with specific prompts and retrieving the generated text.
def ask_chat_model(chat_model, prompt: str):
    response = chat_model.invoke(prompt)
    return response.content