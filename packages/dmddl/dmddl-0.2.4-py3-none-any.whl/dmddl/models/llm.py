import requests

def openai_request(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    url = "https://api.openai.com/v1/chat/completions"
    data = {
        'model': 'gpt-4o-mini',
        'messages':[
            {
                'role': 'developer',
                'content': prompt
             }
        ]
    }
    response = requests.post(url=url, headers=headers, json=data)
    try:
        return response.json()['choices'][0]['message']['content']
    except KeyError as e:
        print(f"[red bold] Error: {e}.\n Check output.txt file.")
        return response.json()


