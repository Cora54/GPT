import asyncio
from typing import Any, Dict, List, Tuple

from src.interfaces.connector import ConnectorI, MessageSender, MessageReciever, MessageHandler


class ResultWaiter(ConnectorI):
  waiter: asyncio.Event
  results: List[Tuple[str, Any]]
  handlers: Dict[str, MessageHandler]

  def __init__(self):
    self.waiter = asyncio.Event()
    self.results = []
    self.handlers = {}
  
  def getMessageSender(self, senderId: str) -> MessageSender:
    async def sender(data):
      self.results.append((senderId, data))
      self.waiter.set()
    return sender
  
  def getMessageReciever(self, recieverId: str) -> MessageReciever:
    def saveHandler(handler: MessageHandler):
      self.handlers[recieverId] = handler
    return saveHandler

  async def waitResult(self):
    await self.waiter.wait()
    self.waiter.clear()
    results = self.results[:]
    self.results.clear()
    return results
