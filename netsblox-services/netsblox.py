import json

class types():
    def String(value):
        return str(value)

    def Number(value):
        return float(value)

    def Integer(value):
        return int(value)

    def List(value):
        return value

    def Any(value):
        return value

class RPC():
    def __init__(self, fn, help=''):
        self.help = help
        self.fn = fn
        assert(not isinstance(fn, RPC))
        assert(not isinstance(fn, Argument))
        self.args = []

    def add_argument(self, arg):
        self.args.append(arg)

    def partial(fn, arg=None, help=None):
        rpc = fn if isinstance(fn, RPC) else RPC(fn)
        if arg is not None:
            rpc.args.insert(0, arg)

        if help is not None:
            rpc.help = help

        return rpc

    def metadata(self):
        metadata = {}
        metadata['name'] = self.fn.__name__
        metadata['description'] = self.help
        metadata['args'] = [ arg.metadata() for arg in self.args ]
        return metadata

    def __call__(self, arg_data):
        self.ensure_valid_args(arg_data)
        args = {}
        for arg in self.args:
            arg_exists = arg_data[arg.name] != ''
            if arg_exists:
                args[arg.name] = arg.parse(arg_data[arg.name])

        return self.fn(**args)

    def ensure_valid_args(self, arg_data):
        args = []
        missing_args = []
        for arg in self.args:
            content = arg_data[arg.name]
            arg_exists = content != ''
            if not arg.optional and not arg_exists:
                missing_args.append(arg.name)

        if len(missing_args) > 0:
            msg = '\n'.join([f'"{arg}" is required.' for arg in missing_args])
            raise Exception(msg)

class Argument():
    def __init__(self, name, help, type, optional=False):
        self.name = name
        self.help = help
        self.type = type
        self.optional = optional

    def metadata(self):
        metadata = {}
        metadata['name'] = self.name
        metadata['description'] = self.help
        metadata['optional'] = self.optional
        return metadata

    def parse(self, value):
        try:
            return self.type(value)
        except Exception as e:
            raise Exception(f'"{self.name}" is not a valid {self.type.__name__}')

def rpc(help):
    return lambda fn: RPC.partial(fn, help=help)

def argument(name, help='', type=types.Any, optional=False):
    arg = Argument(name, help, type, optional)
    return lambda fn: RPC.partial(fn, arg=arg)

