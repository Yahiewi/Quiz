import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("DEEPSEEK_API_KEY")
url = "https://api.deepseek.com/v1/chat/completions"

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Generate a simple quiz question about JavaScript with 4 answers."}
    ],
    "temperature": 0.7,
    "max_tokens": 500
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
print(response.json())