from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import json
import sys
from os.path import dirname
current_dir = dirname(__file__)
sys.path.append(current_dir)

app = Flask(__name__)
CORS(app)

from services import Services
services = Services()

@app.route('/')
def services_metadata():
    return jsonify(services.metadata())

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/<service>')
def service_metadata(service):
    service = services.get(service)
    return jsonify(service.metadata)

@app.route('/<service>/<rpc>', methods=['POST'])
def invoke_rpc(service, rpc):
    username = request.args.get('username')
    print(f'{service}.{rpc}(<omitted>) invoked by {username}')
    service = services.get(service)
    arg_data = request.json
    try:
        return json.dumps(service.invoke_rpc(rpc, arg_data))
    except Exception as e:
        return str(e), 500
