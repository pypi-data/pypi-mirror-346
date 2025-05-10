import requests

def answer(question, role="user"):
    dictToSend = {"model": "gpt-4o-mini", "request": {"messages": [{"role": role, "content": question}]}}
    res = requests.post('https://api.onlysq.ru/ai/v2', json=dictToSend)
    response = res.json()
    return response["choices"][0]["message"]["content"]

