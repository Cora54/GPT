from src.environment import environment
from src.database.service import DBSqlAlchemy
from .gpt import makeQuestions
import json


def setup() -> DBSqlAlchemy:
  dbConnector = DBSqlAlchemy(environment.databaseUrl)
  return dbConnector


themes = [
  'Введение в PHP: основные понятия и преимущества языка',
  'Установка и настройка PHP на сервере',
  'Синтаксис языка PHP: переменные, операторы, условные конструкции, циклы',
  'Работа с массивами и строками в PHP',
  'Функции и область видимости в PHP',
  'Работа с файлами и директориями в PHP',
  'Работа с базами данных в PHP: подключение, выполнение SQL-запросов, обработка результатов',
  'Обработка форм и передача данных между скриптами с помощью GET и POST запросов',
  'Работа с сессиями и куками в PHP',
  'Обработка и валидация данных на стороне сервера',
  'Разработка объектно-ориентированных приложений на PHP',
  'Работа с API и веб-сервисами: отправка и получение данных через HTTP-запросы',
  'Обработка исключений и ошибок в PHP',
  'Шаблонизация и работа с шаблонами в PHP',
  'Оптимизация производительности PHP-скриптов: кэширование, оптимизация SQL-запросов и кода',
  'Разработка безопасных веб-приложений на PHP: защита от атак, обработка пользовательского ввода',
  'Интеграция PHP с другими технологиями: JavaScript, Ajax, XML, JSON',
  'Создание и использование пользовательских расширений и библиотек на PHP',
  'Развертывание и управление проектом на PHP с использованием инструментов разработки и контроля версий',
  'Советы и практические рекомендации по разработке на PHP',
]

help = '''
Для загрузки тем из файла share/themes.txt введите [loadThemes]
Для вывода списка тем введите [showThemes]
Для генерации вопросов введите [generateQuestions]
Для вывода вопросов введите [showQuestions]
Для выхода введите [exit]
'''


async def loadThemes(dbConnector: DBSqlAlchemy):
  try:
    with open('share/themes.txt', 'r', encoding='utf8') as f:
      themes = f.read()
  except:
    print('Не найден файл')
    return
  themes = themes.strip().split('\n')
  for themeNameRaw in themes:
    themeName = themeNameRaw.strip()
    if themeName == '':
      continue
    foundThemes = await dbConnector.getThemeByName(themeName)
    if len(foundThemes) > 0:
      print('Уже существует:', themeName)
      continue
    await dbConnector.saveTheme(themeName)
  print('Темы загружены!')


async def showThemes(dbConnector: DBSqlAlchemy):
  themes = await dbConnector.getThemes()
  print()
  print('Темы:')
  print('VVV')
  for theme in themes:
    print(f'[{theme["id"]}]', theme['name'])
  print('^^^')


async def showQuestions(dbConnector: DBSqlAlchemy):
  themeId = input('Введите id темы >')
  if not themeId:
    return
  questions = await dbConnector.getQuestionsByThemeId(themeId)
  print()
  print('Вопросы:')
  print('VVV')
  for question in questions:
    print(f'''Вопрос [{
      question['id']
    }] {
      'с кодом' if question['hasCode'] else 'без кода'
    } с ответом ({
      question['answer']
    })''')
    print(question['question'])
    print('-----')
  print('^^^')


async def generateQuestions(dbConnector: DBSqlAlchemy):
  themeId = input('Введите id темы >')
  if not themeId:
    return
  themes = await dbConnector.getThemeById(themeId)
  if len(themes) == 0:
    print('Тема не найдена!')
    return
  hasCode = input('С кодом (Y) или без (по умолчанию) >') == 'Y'
  result = makeQuestions(themes[0]['name'], themes[0]['id'], hasCode)
  print(f'Сгенерировано {len(result)} вопросов')
  for question in result:
    await dbConnector.saveQuestion(question)
  print('Вопросы сохранены!')


async def run():
  dbConnector = setup()
  while True:
    print(help)
    v = input('>')
    if v == 'loadThemes':
      await loadThemes(dbConnector)
      continue
    if v == 'showThemes':
      await showThemes(dbConnector)
      continue
    if v == 'generateQuestions':
      await generateQuestions(dbConnector)
      continue
    if v == 'showQuestions':
      await showQuestions(dbConnector)
      continue
    if v == 'exit':
      break
  # result = makeQuestions(themes[3], 'themeId', False)
  # print(json.dumps(result, ensure_ascii=False, indent=2))
