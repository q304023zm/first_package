import re
import yaml
import os
import importlib

def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']

def http405(env, start_response):
    start_response('405 Method Not Allowed', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'405 Method Not Allowed']

class Router:

    def __init__(self):
        self.routes = []
        self.routing_file_path = os.path.join(os.path.dirname(__file__), 'input.yml')

    def register(self, callback):
        f = open(self.routing_file_path, "r+")
        routing = yaml.safe_load(f)
        for r in routing:
            m = importlib.import_module(routing[r]['module'])
            self.routes.append({
                'method': routing[r]['method'],
                'path': routing[r]['url'],
                'path_compiled': re.compile(routing[r]['url']),
                'callback': getattr(m, routing[r]['action'])
            })

    def match(self, method, path):
        error_callback = http404
        for r in self.routes:
            matched = r['path_compiled'].match(path)
            if not matched:
                continue
            error_callback = http405
            url_vars = matched.groupdict()
            if method == r['method']:
                return r['callback'], url_vars
        return error_callback, {}