import datetime
from typing import Dict, List, Union
from sqlalchemy import select, insert, delete, func, update

from .base import DatabaseAdapter
from .models import *
from .types import IdInfo, QuestionData, QuestionEntity, ThemeEntity
from .gen_uuid import gen_uuid


class DBSqlAlchemy:
  dbAdapter: DatabaseAdapter

  def __init__(self, databaseUrl: str):
    self.dbAdapter = DatabaseAdapter(databaseUrl)

  async def saveTheme(self, themeName: str) -> IdInfo:
    id = gen_uuid()
    async with self.dbAdapter.getSession() as session, session.begin():
      await session.execute(
        insert(Theme).values(
          id=id,
          name=themeName,
        )
      )
      return {
        'id': id,
      }

  async def saveQuestion(self, questionData: QuestionData):
    id = gen_uuid()
    async with self.dbAdapter.getSession() as session, session.begin():
      await session.execute(
        insert(Question).values(
          id=id,
          themeId=questionData['themeId'],
          question=questionData['question'],
          answer=questionData['answer'],
          hasCode=questionData['hasCode'],
        )
      )
      return {
        'id': id,
      }

  async def getThemes(self) -> List[ThemeEntity]:
    async with self.dbAdapter.getSession() as session, session.begin():
      result = await session.execute(
        select(
          Theme.id,
          Theme.name,
        ).limit(1000)
      )
      return [{
        'id': row[0],
        'name': row[1],
      } for row in result]

  async def getThemeByName(self, name: str) -> List[ThemeEntity]:
    async with self.dbAdapter.getSession() as session, session.begin():
      result = await session.execute(
        select(
          Theme.id,
          Theme.name,
        ).where(Theme.name == name)
        .limit(1)
      )
      return [{
        'id': row[0],
        'name': row[1],
      } for row in result]

  async def getThemeById(self, themeId: str) -> List[ThemeEntity]:
    async with self.dbAdapter.getSession() as session, session.begin():
      result = await session.execute(
        select(
          Theme.id,
          Theme.name,
        ).where(Theme.id == themeId)
        .limit(1)
      )
      return [{
        'id': row[0],
        'name': row[1],
      } for row in result]

  async def getQuestionsByThemeId(self, themeId: str) -> List[QuestionEntity]:
    async with self.dbAdapter.getSession() as session, session.begin():
      result = await session.execute(
        select(
          Question.id,
          Question.question,
          Question.answer,
          Question.hasCode,
        ).where(Question.themeId == themeId)
        .limit(100)
      )
      return [{
        'id': row[0],
        'question': row[1],
        'answer': row[2],
        'hasCode': row[3],
        'themeId': themeId,
      } for row in result]


  # async def getUserProfile(self, guestId: str = None, phone: str = None) -> Dict | None:
  #   if guestId is not None:
  #     cond = User.id == guestId
  #   elif phone is not None:
  #     cond = User.phone == phone
  #   else:
  #     return None
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       select(
  #         User.id,
  #         User.name,
  #         User.surName,
  #         User.phone,
  #         User.sex,
  #         User.email,
  #         User.birthday,
  #         User.broadcastOffer,
  #         User.pushTokens,
  #         User.bonuses,
  #       ).where(cond)
  #       .limit(1)
  #     )
  #     result = result.all()
  #   if len(result) == 0:
  #     return None
  #   return {
  #     'id': result[0][0],
  #     'name': result[0][1],
  #     'surName': result[0][2],
  #     'phone': result[0][3],
  #     'sex': result[0][4],
  #     'email': result[0][5],
  #     'birthday': result[0][6],
  #     'broadcastOffer': result[0][7],
  #     'pushTokens': result[0][8],
  #     'bonuses': result[0][9],
  #   }

  # async def createUserProfile(self, guestId: str, regUser: RegistrationUser, name: str, surName: str, birthday: datetime.date | None, sex: str) -> Union[Dict, None]:
  #   """Создание профиля клиента"""
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       insert(User).returning(User.id).values(
  #         id=guestId,
  #         name=name,
  #         surName=surName,
  #         phone=regUser.phone,
  #         sex=sex,
  #         birthday=birthday,
  #       )
  #     )
  #     result = result.all()
  #     return {
  #       'id': result[0][0],
  #     }

  # async def updateUserProfile(self, user: User, bonusesDelta: float = None) -> Union[Dict, None]:
  #   """Обновляет данные профиля клиента"""
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     prevBonusesInfo = await session.execute(
  #       select(
  #         User.id,
  #         User.bonuses,
  #       ).where(
  #         User.id == user.id,
  #       )
  #     )
  #     prevBonusesInfo = prevBonusesInfo.all()
  #     if len(prevBonusesInfo) == 0:
  #       return None
  #     prevBonuses = prevBonusesInfo[0][1]
  #     if prevBonuses is None:
  #       prevBonuses = 0
  #     if bonusesDelta is not None:
  #       newBonuses = prevBonuses + bonusesDelta
  #     else:
  #       newBonuses = prevBonuses
  #     if newBonuses < 0:
  #       return None
  #     await session.execute(
  #       update(
  #         User
  #       ).where(
  #         User.id == user.id,
  #       ).values(
  #         id=user.id,
  #         name=user.name,
  #         surName=user.surName,
  #         phone=user.phone,
  #         sex=user.sex,
  #         email=user.email,
  #         birthday=user.birthday,
  #         broadcastOffer=user.broadcastOffer,
  #         bonuses=newBonuses,
  #       )
  #     )
  #   return await self.getUserProfile(user.id)

  # async def getGuestTable(self, guestId: str) -> Union[Dict, None]:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       select(TablePlace.id, Table.id, Table.cafeId, Table.code, Table.number, Table.placesCount)
  #       .where(TablePlace.guestId == guestId)
  #       .limit(1)
  #       .join(TablePlace, Table.id == TablePlace.tableId)
  #     )
  #     result = result.all()
  #   if len(result) == 0:
  #     return None
  #   return {
  #     'id': result[0][1],
  #     'cafeId': result[0][2],
  #     'code': result[0][3],
  #     'number': result[0][4],
  #     'placesCount': result[0][5],
  #   }

  # async def getWaiter(self, tableId: str) -> Union[Dict, None]:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       select(Waiter.id, Waiter.name, Waiter.photo)
  #       .select_from(Table)
  #       .where(Table.id == tableId)
  #       .join(Waiter, Waiter.id == Table.waiterId)
  #     )
  #     result = result.all()
  #   if len(result) == 0:
  #     return None
  #   return {
  #     'id': result[0][0],
  #     'name': result[0][1],
  #     'photo': result[0][2],
  #   }

  # async def getTableByCode(self, code: str) -> Union[Dict, None]:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       select(Table.id, Table.cafeId, Table.number, Table.placesCount)
  #       .where(Table.code == code)
  #       .limit(1)
  #     )
  #     result = result.all()
  #   if len(result) == 0:
  #     return None
  #   return {
  #     'id': result[0][0],
  #     'cafeId': result[0][1],
  #     'number': result[0][2],
  #     'placesCount': result[0][3],
  #   }
  
  # async def getTablePlaces(self, tableId: str) -> Dict:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     places = await session.execute(
  #       select(func.count(TablePlace.id))
  #       .where(TablePlace.tableId == tableId)
  #     )
  #     places = places.all()
  #   return {
  #     'currentPlaces': places[0][0],
  #   }
  
  # async def setNewTableForGuest(self, guestId: str, tableId: str) -> Dict:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       insert(TablePlace).returning(TablePlace.id).values(
  #         tableId=tableId,
  #         guestId=guestId,
  #       )
  #     )
  #     result = result.all()
  #   return {}
  
  # async def removeTableForGuest(self, guestId: str, tableId: str) -> None:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     await session.execute(
  #       delete(TablePlace)
  #       .where(TablePlace.guestId == guestId)
  #       .where(TablePlace.tableId == tableId)
  #     )

  # def getFabricCRUD(self) -> CRUDFabric:
  #   return getFabricCRUD(self.dbAdapter)

  # # --

  # async def createWaiter(self, waiter: Waiter) -> Dict:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       insert(Waiter).returning(Waiter.id).values(
  #         name=waiter.name,
  #         photo=waiter.photo,
  #       )
  #     )
  #     result = result.all()
  #   return {
  #     'id': result[0][0],
  #   }

  # async def createTable(self, waiterId: str, table: TableModel) -> Dict:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       insert(Table).returning(Table.id).values(
  #         waiterId=waiterId,
  #         code=table.code,
  #         cafeId=table.cafeId,
  #         number=table.number,
  #         placesCount=table.placesCount,
  #       )
  #     )
  #     result = result.all()
  #   return {
  #     'id': result[0][0],
  #   }

  # async def createRegistrationUser(self, guest: Guest, phone: str, code: str | None) -> Dict:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       insert(RegistrationUser).returning(
  #         RegistrationUser.phone,
  #         RegistrationUser.verificationCode,
  #         RegistrationUser.isConfirmed,
  #       ).values(
  #         guestId=guest.id,
  #         phone=phone,
  #         verificationCode=code,
  #         isConfirmed=False,
  #       )
  #     )
  #     result = result.all()
  #     return {
  #       'phone': result[0][0],
  #       'verificationCode': result[0][1],
  #       'isConfirmed': result[0][2],
  #     }

  # async def getRegistrationUser(self, guestId: str) -> Dict | None:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     registrationUser = await session.execute(
  #       select(
  #         RegistrationUser.phone,
  #         RegistrationUser.verificationCode,
  #         RegistrationUser.isConfirmed,
  #       )
  #       .where(RegistrationUser.guestId == guestId)
  #       .limit(1)
  #     )
  #     result = registrationUser.all()
  #     if len(result) == 0:
  #       return None
  #     return {
  #       'phone': result[0][0],
  #       'verificationCode': result[0][1],
  #       'isConfirmed': result[0][2],
  #     }

  # async def updateRegistrationUserConfirmCode(self, guestId: str, newPhone: str, newCode: str) -> None:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     await session.execute(
  #       update(RegistrationUser)
  #       .where(RegistrationUser.guestId == guestId)
  #       .values(
  #         verificationCode=newCode,
  #         phone=newPhone,
  #         isConfirmed=False,
  #       )
  #     )

  # async def confirmRegistrationUser(self, regUser: RegistrationUser) -> bool:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     await session.execute(
  #       update(RegistrationUser)
  #       .where(RegistrationUser.guestId == regUser.id)
  #       .values(
  #         isConfirmed=True,
  #       )
  #     )
  #     return await self.getRegistrationUser(regUser.id) is not None
  
  # async def getUsersByPushToken(self, token: str) -> List[Dict]:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     result = await session.execute(
  #       select(
  #         User.id,
  #         User.pushTokens,
  #       )
  #       .where(User.pushTokens.contains([token]))
  #     )
  #   return [
  #     {
  #       'id': userRaw[0],
  #       'pushTokens': userRaw[1],
  #     } for userRaw in result
  #   ]

  # async def updateUserPushTokens(self, userId: str, tokens: List[str]) -> None:
  #   async with self.dbAdapter.getSession() as session, session.begin():
  #     await session.execute(
  #       update(User)
  #       .where(User.id == userId)
  #       .values(
  #         pushTokens=tokens,
  #       )
  #     )
