import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.deportista_model import DeportistaModel
from botocore.exceptions import ClientError

class DynamoDbInterface:
    def create_table(self):
        raise NotImplementedError
    
    def insert_item(self,deportista: DeportistaModel):
        raise NotImplementedError
    
    def get_item(self,id_deportista):
        raise NotImplementedError
  
    def tablaExits(self,name):
        raise NotImplementedError
    
    def deleteTable(self):
        raise NotImplementedError    
       

class DynamoDbDeportista(DynamoDbInterface):
    def __init__(self,dynamodb=None):        
        # Crear una instancia de cliente DynamoDB
        if dynamodb is None:
            self.dynamodb = boto3.client('dynamodb',
                                    region_name='us-east-1',
                                    aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                    aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        else:
            self.dynamodb = dynamodb

        self.table_name = 'deportista'

    # Funciones para interactuar con DynamoDB
    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_usuario',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_usuario',
                            'KeyType': 'HASH'  # Clave de partición
                        }
                    ],        
                    BillingMode='PAY_PER_REQUEST'
                )
            
            # Espera hasta que la tabla exista
            self.dynamodb.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f'Tabla {self.table_name} creada correctamente.')
        else:
            print(f"La tabla '{self.table_name}' ya existe.")

    def insert_item(self,deportista: DeportistaModel):
        item = {
            "id_usuario": {'S':  deportista.id_usuario },
            "nombre": {'S': deportista.nombre },
            "apellido": {'S': deportista.apellido },
            "tipo_identificacion": {'S': deportista.tipo_identificacion },
            "numero_identificacion": {'S': deportista.numero_identificacion },
            'genero': {'S': deportista.genero },
            'edad': {'N': str(deportista.edad)},
            'peso_inicial': {'N': str(deportista.peso_inicial)},
            'peso_actual': {'N': str(deportista.peso_actual)},
            'altura': {'N': str(deportista.altura)},
            'pais_residencia': {'S': deportista.pais_residencia},
            'ciudad_residencia': {'S': deportista.ciudad_residencia},
            'pais_nacimiento': {'S': deportista.pais_nacimiento},
            'ciudad_nacimiento': {'S': deportista.ciudad_nacimiento},
            'deporte_practicar': {'S': deportista.deporte_practicar},
            'plan': {'S': deportista.plan}, # 'Gratuito', 'Intermedio', 'Premium
            'fecha_creacion': {'S': str(deportista.fecha_creacion)}  # Datetime conversion
            
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_item(self,id_usuario):
        key = {
            'id_usuario': {'S': str(id_usuario) }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None
        
        # Extrae los valores de cada campo
        id_usuario = item['id_usuario']['S']
        nombre = item['nombre']['S']
        apellido = item['apellido']['S']
        tipo_identificacion = item['tipo_identificacion']['S']
        numero_identificacion = item['numero_identificacion']['S']
        genero = item['genero']['S']
        edad = int(item['edad']['N'])
        peso_inicial = float(item['peso_inicial']['N'])
        peso_actual = float(item['peso_actual']['N'])
        altura = float(item['altura']['N'])
        pais_residencia = item['pais_recidencia']['S']
        ciudad_residencia = item['ciudad_recidencia']['S']
        deporte_practicar = item['deporte_practicar']['S']
        pais_nacimiento = item['pais_nacimiento']['S']
        ciudad_nacimiento = item['ciudad_nacimiento']['S']
        plan = item['plan']['S']
        fecha_creacion = item['fecha_creacion']['S']

        # Crea una instancia de la clase Entrenamiento
        deportista = DeportistaModel(id_usuario,nombre,apellido,tipo_identificacion,numero_identificacion,genero,edad,peso_inicial, peso_actual, altura,pais_residencia,pais_nacimiento,ciudad_nacimiento,ciudad_residencia,deporte_practicar, plan, fecha_creacion)

        return deportista
    
    def update_plan(self, id_usuario, new_plan):
        key = {
            'id_usuario': {'S': str(id_usuario) }  # Clave de búsqueda
        }
        update_expression = "SET #p = :val"
        expression_attribute_names = {
            '#p': 'plan'
        }
        expression_attribute_values = {
            ':val': {'S': new_plan}
        }
        response = self.dynamodb.update_item(
            TableName=self.table_name,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        print('Plan actualizado correctamente.')
        return response
    
    def tablaExits(self,name):
        try:
            response = self.dynamodb.describe_table(TableName=name)
            print(response)
            return True
        except ClientError as err:
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                return False

    def deleteTable(self):
        # Eliminar la tabla
        self.dynamodb.delete_table(TableName=self.table_name)

        # Esperar hasta que la tabla no exista
        self.dynamodb.get_waiter('table_not_exists').wait(TableName=self.table_name)