from typing import List
from ..database.types import QuestionData
from .utils import questionsDelim, answerDelim

def parseAnswer(answer: str, themeId: str):
  questions = answer.split(questionsDelim)
  questionsData: List[QuestionData] = []
  for question in questions:
    if question.strip() == '':
      continue
    qa = question.split(answerDelim)
    if len(qa) < 2:
      print('Incorrect 1')
      print('VVVVV')
      print(question)
      print('^^^^^')
      continue
    clearQuestion = qa[0].strip()
    numberPos = clearQuestion.find('.')
    if numberPos >= 0 and numberPos < 3:
      clearQuestion = clearQuestion[numberPos+1:].strip()
    hasCode = '```' in clearQuestion
    letters = []
    clearQuestionLines = clearQuestion.split('\n')
    for qLine in clearQuestionLines[::-1]:
      s = qLine.strip()
      if s == '':
        break
      letters.append(s[0])
    clearAnswer = qa[1].strip()
    if clearAnswer == '':
      print('Incorrect 2')
      print('VVVVV')
      print(question)
      print('^^^^^')
      continue
    if clearAnswer[0] == ':':
      clearAnswer = clearAnswer[1:].strip()
    if clearAnswer[0] not in letters:
      print('Incorrect 3')
      print('VVVVV')
      print(question)
      print('^^^^^')
      continue
    questionsData.append(QuestionData(
      themeId=themeId,
      question=clearQuestion,
      answer=clearAnswer[0],
      hasCode=hasCode,
    ))
  return questionsData
