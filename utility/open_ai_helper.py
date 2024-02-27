from openai import OpenAI

from config.config import open_api_config
client = OpenAI(api_key=open_api_config['api_key'])


def openApi(prompt):
    print(prompt, '----')
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": '房仲角色，幽默語氣，繁體中文： ' + prompt}
            ]
        )

        gpt_response = completion.choices[0].message.content

        return gpt_response
    except Exception as e:
        print('open ai error: ', e)
        return None
