#Install werkzeug using pip3
from werkzeug.wrappers import Request, Response

@Request.application
def app(request):
    print(request.path)
    print(request.headers)
    return Response("Hello, World!")

from werkzeug.serving import run_simple
run_simple("localhost", 4000, app)