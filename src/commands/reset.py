from .base_command import BaseCommannd
from ..dynamodb_deportista import DynamoDbDeportista

class Reset(BaseCommannd):
  def __init__(self):
    self.db = DynamoDbDeportista()

  def execute(self):
    self.db.deleteTable()
    self.db.create_table()