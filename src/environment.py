import os
from dotenv import load_dotenv

load_dotenv()


class Stage:
  migrationReady = 'migration_ready'


class Environment:
  databaseUrl: str
  gptToken: str
  stage: str


def getEnv():
  env = Environment()
  env.databaseUrl = os.environ.get('DATABASE_URL', '')
  env.gptToken = os.environ.get('GPT_TOKEN', '')
  env.stage = os.environ.get('STAGE', '')
  return env


environment = getEnv()
