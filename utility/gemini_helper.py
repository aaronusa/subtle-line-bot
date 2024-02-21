import json
import requests

GEMINI_API_KEY = 'AIzaSyCd_7GVAL6h9Ra_N4lUle75hxxJyE9-TyY'


def calling_gemini_api(content):
    data = {
        "contents": [
            {
                "parts": [{"text": f'繁體中文回應 {content}'}]
            }
        ]
    }

    try:
        # url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
        url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            gemini_answer = response.json()
            print(gemini_answer)
            return gemini_answer['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print('open ai error: ', e)
        return None
