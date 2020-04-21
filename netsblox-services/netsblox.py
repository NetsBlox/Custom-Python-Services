class types():
    def String(value):
        return str(value)

    def Number(value):
        return float(value)

class RPC():
    def __init__(self, fn, help=''):
        self.help = help
        self.fn = fn
        print('fn is', fn)
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
        args = [ arg.parse(arg_data[arg.name]) for arg in self.args ]
        return self.fn(*args)

class Argument():
    def __init__(self, name, help, type, optional=False):
        print('creating Argument', name)
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
        return self.type(value)

def rpc(help):
    print('rpc:', help)
    return lambda fn: RPC.partial(fn, help=help)

def argument(name, help, type):
    print('argument:', name)
    arg = Argument(name, help, type)
    return lambda fn: RPC.partial(fn, arg=arg)

