from typing import TypedDict


class IdInfo(TypedDict):
  id: str


class ThemeEntity(IdInfo):
  name: str


class QuestionData(TypedDict):
  themeId: str
  question: str
  answer: str
  hasCode: bool


class QuestionEntity(QuestionData):
  id: str
