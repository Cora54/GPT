from traceback import print_exc
import requests
from ..environment import environment
from time import time
from .utils import apiUrl

def getRequestData(message: str):
  return {
    "model": "gpt-3.5-turbo",
    "messages": [
      # {
      #   "role": "system",
      #   "content": "You are a helpful assistant."
      # },
      {
        "role": "user",
        "content": message
      }
    ]
  }

headers = {
  "Authorization": f"Bearer {environment.gptToken}"
}

def makeRequest(message: str):
  print('Обрабатывается запрос для темы:', message)
  t = time()
  response = requests.post(
    apiUrl,
    json=getRequestData(message),
    headers=headers,
  )
  t = time() - t
  print('Запрос завершен за', t, 'секунд')
  if response.status_code == 200:
    try:
      answerResult: str = response.json()['choices'][0]['message']['content']
    except:
      print_exc()
      return None
  else:
    print("Ошибка:", response.text)
    return None
  return answerResult
