# Load all services and return them
from importlib import import_module
from os.path import basename, dirname, join
import os
from os import path
import sys
from netsblox import RPC
from json import JSONEncoder

def get_service_metadata(module):
    data = {}
    data['description'] = module.__doc__.strip()
    data['categories'] = getattr(module, 'categories', [])
    data['rpcs'] = {}
    for rpc in Service.get_rpcs(module):
        metadata = rpc.metadata()
        data['rpcs'][metadata['name']] = metadata
    return data

class Service():
    def __init__(self, module):
        self.name = Service.get_service_name(module)
        print('creating service:', self.name)
        self.module = module
        self.metadata = get_service_metadata(module)

    def invoke_rpc(self, rpc_name, arg_data):
        rpc = getattr(self.module, rpc_name, None)
        if rpc is None:
            raise Exception('RPC "' + rpc_name + '" is not available.')
        # TODO: Add context info
        return rpc(arg_data)

    def get_service_name(module):
        default_name = Service.get_default_name(module)
        if hasattr(module, 'service_name'):
            return module.service_name
        return default_name

    def get_default_name(module):
        name = module.__name__
        return ''.join((n.capitalize() for n in name.split('_')))

    def get_rpcs(module):
        public_vars = (fn for fn in dir(module) if not fn.startswith('_'))
        public_vals = (getattr(module, v) for v in public_vars)
        return (val for val in public_vals if isinstance(val, RPC))

def is_service_path(filepath):
    services_dir = dirname(__file__)
    fullpath = path.realpath(path.join(services_dir, filepath))
    return not filepath.startswith('_') and path.isdir(fullpath)

class Services():
    def __init__(self):
        services_dir = dirname(__file__)
        sys.path.append(services_dir)
        service_dirs = (dir for dir in os.listdir(services_dir) if is_service_path(dir))
        service_modules = (__import__(name, globals(), locals()) for name in service_dirs)
        self.services = [Service(module) for module in service_modules]

    def metadata(self):
        return [{'name': service.name, 'categories': service.metadata['categories']} for service in self.services]

    def get(self, name):
        service = next((service for service in self.services if service.name == name))
        return service
