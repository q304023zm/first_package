from simplewsgi.router import Router

class SimpleWsgi:
    def __init__(self):
        self.router = Router()

    def load(self, callback=None):
        self.router.register(callback)

    def __call__(self, env, start_response):
        method = env['REQUEST_METHOD'].upper()
        path = env['PATH_INFO'] or '/'
        callback, kwargs = self.router.match(method, path)
        start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
        return callback(env, start_response, **kwargs)