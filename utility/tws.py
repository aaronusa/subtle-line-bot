import json
import requests

MODEL_NAME = "ffm-bloomz-176b"
API_KEY = "5bdf2c29-7db3-4c0b-88b7-14f7b75d78a4"
API_URL = "https://54934.afs.twcc.ai/text-generation/api"

# parameters
max_new_tokens = 350
temperature = 0.5
top_k = 50
top_p = 1.0
frequence_penalty = 1.0


def generate(prompt):
    headers = {
        "content-type": "application/json",
        "X-API-Key": API_KEY}
    data = {
        "model": MODEL_NAME,
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "frequence_penalty": frequence_penalty
        }
    }

    result = ''
    try:
        response = requests.post(
            API_URL + "/models/generate", json=data, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.text, strict=False)['generated_text']
        else:
            print("error")
    except Exception as e:
        print("error", e)
    return result.strip("\n")


result = generate("假裝你是房仲，講一個笑話")
print(result)
