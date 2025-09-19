# 代码生成时间: 2025-09-20 03:29:09
from pyramid.config import Configurator
from pyramid.response import Response
import psutil
import json

# Define the root factory for the application
def system_performance_monitor(request):
    # Fetch system information using psutil
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_io = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

    # Create a dictionary with the system information
    system_info = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "network_io": network_io,
    }

    # Return the system information as a JSON response
    return Response(json.dumps(system_info), content_type='application/json')

# Configure the Pyramid application
def main(global_config, **settings):
    """ This function sets up the Pyramid WSGI application. """
    config = Configurator(settings=settings)

    # Add the endpoint for the system performance monitor
    config.add_route('system_performance', '/system-performance')
    config.add_view(system_performance_monitor, route_name='system_performance')

    # Scan for @view_config decorators and apply them
    config.scan()

    # Return the WSGI application
    return config.make_wsgi_app()

# In a production environment, you would use an ASGI or WSGI server to serve this application.
# For development, you can use the development server provided by Pyramid by uncommenting the following line:
# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     server = make_server('0.0.0.0', 6543, main(global_config={ }))
#     server.serve_forever()