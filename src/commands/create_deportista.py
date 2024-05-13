import uuid
from .base_command import BaseCommannd
from ..models.deportista_model import DeportistaModel
from ..errors.errors import IncompleteParams, ClientInvalidParameterError, SportmanAlreadyExists
from ..dynamodb_deportista import DynamoDbDeportista
from datetime import datetime

class CreateDeportista(BaseCommannd):
  def __init__(self, data):
    self.data = data
    self.db = DynamoDbDeportista()
  
  def execute(self):
    try:
      
      posted_deportista = DeportistaModel(self.data['id_usuario'],self.data["nombre"], self.data["apellido"], self.data['tipo_identificacion'], self.data['numero_identificacion'],
                                          self.data['genero'], self.data['edad'],  self.data['peso_inicial'], self.data['peso_inicial'],self.data['altura'],
                                          self.data['pais_recidencia'], self.data['ciudad_recidencia'],self.data['deporte_practicar'], '', datetime.now())
      
      print(posted_deportista)
      
      if not self.verificar_datos(self.data['id_usuario']):
         raise ClientInvalidParameterError
      
      if self.deportista_exist(self.data['id_usuario']):
        raise SportmanAlreadyExists()

      self.db.insert_item(posted_deportista)

      return posted_deportista
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def deportista_exist(self, id_usuario):
    result =  self.db.get_item(id_usuario)
    if result is None:
      return False
    else:
      return True
      
  def verificar_datos(self,id_usuario):
    if id_usuario and id_usuario.strip():
        return True
    else:
        return False