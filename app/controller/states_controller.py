from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from ..service.states_service import StateService

api = Namespace('Estados', "Endpoint com informações sobre os estados.")

service = StateService()

@api.route("")
class StatesList(Resource):
    def get(self):
        '''
        Retorna os estados disponíveis
        '''

        return jsonify({'response':
        {
            'code': '200',
            'message': 'Sucesso',
            'body': service.get_states()
        }
        })

@api.route("/<string:state>/data")
@api.doc(params={'state': 'estado que quer se obter os dados'})
class State(Resource):
    def get(self, state):
        '''
        Retorna os dados sobre o determinado estado
        '''

        state = request.args.get("state", "", str)

        return jsonify({'response': 
        {
            'code': '200',
            'message': 'Sucesso',
            'body': service.get_state_info(state)
        }
        })        
