from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, SportmanAlreadyExists,IncompleteParams,ExeptionCognitoCustomError
from ..dynamodb_deportista import DynamoDbDeportista
from botocore.exceptions import ClientError

class UpdatePlanDeportista (BaseCommannd):
  def __init__(self, id_deportista, data):
    
    if id_deportista and id_deportista.strip():
        self.id_deportista = id_deportista
    else:
        raise InvalidParams()
      
    required_fields = ['new_plan']
    if not all(field in data for field in required_fields):
        raise IncompleteParams()
    
    self.data = data
    self.db = DynamoDbDeportista()
    
  def execute(self):
    try:
        if not self.deportista_exist(self.id_deportista):
            raise ExeptionCognitoCustomError(412, "Deportista no existe")
            
        result  = self.db.update_plan(self.id_deportista,self.data['new_plan'])
                
        return result
    
    except ClientError as err:    
        print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
        http_code = err.response['ResponseMetadata']['HTTPStatusCode']
        message =  err.response['Error']['Code'] + '.' + err.response['Error']['Message']      
        raise ExeptionCognitoCustomError(http_code, message)

  def deportista_exist(self, id_usuario):
       result =  self.db. get_item(id_usuario)
       if result is None:
          return False
       else:
          return True