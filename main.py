import asyncio
import os

from src.environment import environment, Stage
from src.setup import run


async def main():
  if environment.stage == Stage.migrationReady:
    pass
  else:
    os.system('alembic upgrade head')
    await run()
  while True:
    await asyncio.sleep(60)


if __name__ == '__main__':
  asyncio.run(main())
