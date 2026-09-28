import requests


def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "gemma3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        return "Error: Ollama AI response failed"


if __name__ == "__main__":
    answer = ask_ai(
        "Explain Artificial Intelligence in two simple sentences."
    )

    print(answer)