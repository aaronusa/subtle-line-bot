import json
import requests

MODEL_NAME = "ffm-bloomz-7b"
API_KEY = "092da750-5ba5-4438-aaf6-b905af78dd3c"
API_URL = "https://55263.afs.twcc.ai/text-generation/api"

# parameters
max_new_tokens = 350
temperature = 0.5
top_k = 50
top_p = 1.0
frequence_penalty = 1.0


def twcc_generate(prompt):
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
            return result
        else:
            print("error")
    except Exception as e:
        print("error", e)
    return result.strip("\n")