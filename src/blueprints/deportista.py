from flask import Flask, jsonify, request, Blueprint
from ..commands.create_deportista import CreateDeportista
from ..commands.get_deportista import GetDeportista
from ..commands.reset import Reset
from ..commands.update_plan_deportista import UpdatePlanDeportista

deportista_blueprint = Blueprint('deportista', __name__)

@deportista_blueprint.route('/deportista', methods = ['POST'])
def create():
    deportista = CreateDeportista(request.get_json()).execute()
    return jsonify(deportista), 201

@deportista_blueprint.route('/deportista/<id>', methods = ['GET'])
def show(id):
    """ Authenticate(auth_token()).execute() """
    deportista = GetDeportista(id).execute() 
    return jsonify(deportista)

@deportista_blueprint.route('/deportista/<id>', methods = ['PATCH'])
def actualizar_plan(id):
    """ Authenticate(auth_token()).execute() """
    deportista = UpdatePlanDeportista(id,request.get_json()).execute() 
    return jsonify(deportista)

@deportista_blueprint.route('/deportista/ping', methods = ['GET'])
def ping():
    return 'pong'

@deportista_blueprint.route('/deportista/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({'status': 'OK'})

def auth_token():
    if 'Authorization' in request.headers:
        authorization = request.headers['Authorization']
    else:
        authorization = None
    return authorization