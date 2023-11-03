from .req import makeRequest
from .parse import parseAnswer
from .utils import questionsDelim, countQuestions, answerDelim

def makeQuestions(theme: str, themeId: str, hasCode: bool):
  if hasCode:
    themeRequest = f'Создать сложный тест с вариантами ответа по теме "PHP: {theme}". В заданиях спрашивать результат выполнения кода на PHP. Сделать {countQuestions} вопросов. После каждого вопроса написать "{answerDelim}", правильный вариант ответа и со следующей строки написать "{questionsDelim}"'
  else:
    themeRequest = f'Создать сложный тест с вариантами ответа по теме "PHP: {theme}". Сделать {countQuestions} вопросов. После каждого вопроса написать "{answerDelim}", правильный вариант ответа и со следующей строки написать "{questionsDelim}"'
  response = makeRequest(themeRequest)
  print('VVV')
  print(response)
  print('^^^')
  if not response:
    return None
  # with open('src/ttt4.txt', 'r', encoding='utf8') as f:
  #   response = f.read()
  return parseAnswer(response, themeId)
