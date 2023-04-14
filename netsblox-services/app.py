import base64
import io
from pprint import pprint
from services import Services
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask import request
import json
import sys
from os.path import dirname
current_dir = dirname(__file__)
sys.path.append(current_dir)

app = Flask(__name__)
CORS(app)

services = Services()


@app.route('/')
def services_metadata():
    return jsonify(services.metadata())


@app.route('/favicon.ico')
def favicon():
    return ''


@app.route('/<service>')
def service_metadata(service):
    try:
        service = services.get(service)
        return jsonify(service.metadata)
    except Exception as e:
        return str(e), 500


@app.route('/<service>/<rpc>', methods=['POST'])
def invoke_rpc(service, rpc):
    username = request.args.get('username')
    print(f'{service}.{rpc}(<omitted>) invoked by {username}')
    try:
        service = services.get(service)
        arg_data = request.json

        if service.metadata['rpcs'][rpc]['image']:
            print("image")
            data = service.invoke_rpc(rpc, arg_data)

            data = base64.b64decode(data.encode('utf-8'))
            # buf = io.BytesIO(bytes(data, encoding='utf-8'))
            buf = io.BytesIO(data)
            buf.seek(0)
            return send_file(buf, mimetype="image/png")
        else:
            return json.dumps(service.invoke_rpc(rpc, arg_data))

    except Exception as e:
        return str(e), 500
