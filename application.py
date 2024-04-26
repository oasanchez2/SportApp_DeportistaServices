from flask import Flask, jsonify
from src.blueprints.deportista import deportista_blueprint
from src.errors.errors import ApiError
from flask_cors import CORS
from src.dynamodb_deportista import DynamoDbDeportista

application = Flask(__name__)
application.register_blueprint(deportista_blueprint)
CORS(application)
dynamo_db_entrenamiento = DynamoDbDeportista()
dynamo_db_entrenamiento.create_table()
## add comment
@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description 
    }
    return jsonify(response), err.code
##
if __name__ == "__main__":
    application.run(host="0.0.0.0", port = 5004, debug = True)