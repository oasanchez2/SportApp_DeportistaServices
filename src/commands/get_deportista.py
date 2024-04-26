from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, SportmanNotFoundError
from ..dynamodb_deportista import DynamoDbDeportista

class GetDeportista (BaseCommannd):
  def __init__(self, id_deportista):
    if id_deportista and id_deportista.strip():
      self.id_deportista = id_deportista
    else:
      raise InvalidParams()
    
    self.db = DynamoDbDeportista()
  
  def execute(self):

    result  = self.db.get_item(self.id_deportista)
    if result is None:
      raise SportmanNotFoundError()
    
    return result