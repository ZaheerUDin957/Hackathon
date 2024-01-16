# OpenAI_key.py
import toml

def load_openai_key():
    secrets = toml.load("secrets.toml")
    return secrets.get("openai_api_key", "")

def save_openai_key(api_key):
    secrets = {"openai_api_key": api_key}
    with open("secrets.toml", "w") as file:
        toml.dump(secrets, file)

def update_openai_key(new_api_key):
    save_openai_key(new_api_key)
    OpenAIKey.key = new_api_key

class OpenAIKey:
    key = load_openai_key()
