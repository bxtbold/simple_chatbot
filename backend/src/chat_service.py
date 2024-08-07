import requests
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Define the URL and the payload

try:
    URL = os.environ["OLLAMA_URL"]
    MODEL = os.environ["LLM_MODEL"]
except KeyError:
    print(".env is not set.")
    URL = "http://localhost:11434/api/chat"
    MODEL = "llama3.1"
    print("Setting OLLAMA_URL and LLMA_MODEL to default values.")
    print(f"OLLAMA_URL: {URL}, LLM_MODEL: {MODEL}")

chat_history = []


def validate_history() -> bool:
    global chat_history
    for i in chat_history:
        if not isinstance(i, Dict):
            print(type(i), i)
            return False
        role = i.get("role")
        content = i.get("content")

        if not (role and content):
            print("History is not valid!")
            return False
    return True


def create_payload() -> Dict[str, any]:
    global chat_history
    if validate_history():
        return {
            "model": MODEL,
            "messages": chat_history,
            "stream": False,
            "option": {
                "seed": 42,
            }
        }
    return {}


def add_chat_to_history(content: str, role: str) -> List[Dict[str, str]]:
    global chat_history
    chat = {
        "role": role,
        "content": content
    }
    chat_history.append(chat)


def chat_service(user_content):
    add_chat_to_history(user_content, "user")
    payload = create_payload()

    try:
        # Request the server
        response = requests.post(URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        response_content = response_json["message"]["content"]
        add_chat_to_history(response_content, "assistant")
        return response_content
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.RequestException as err:
        print("Error:", err)
