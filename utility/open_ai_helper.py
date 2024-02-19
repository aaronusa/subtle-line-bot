from openai import OpenAI

from config.config import open_api_config
client = OpenAI(api_key=open_api_config['api_key'])


def openApi(prompt):
    try:
        # completion = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": '假裝我是一個房仲 '+prompt}
        #     ]
        # )
        # gpt_response = completion.choices[0].message.content

        return 'gpt_response'
    except Exception as e:
        print('open ai error: ', e)
        return None
