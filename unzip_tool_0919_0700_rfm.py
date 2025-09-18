# 代码生成时间: 2025-09-19 07:00:50
import os
import zipfile
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPInternalServerError

# Define a view function to handle the unzipping process
@view_config(route_name='unzip', renderer='json')
def unzip_view(request):
    # Get the file path from the request
    file_path = request.matchdict['file_path']
    
    # Ensure the file path is valid
    if not os.path.exists(file_path):
        return {'error': 'File not found'}
        
    # Define the destination directory
    destination_dir = os.path.splitext(file_path)[0]
    
    # Ensure the destination directory does not already exist
    if os.path.exists(destination_dir):
        return {'error': 'Destination directory already exists'}
        
    try:
        # Unzip the file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
            
        # Return a success message
        return {'message': f'Files successfully unzipped to {destination_dir}'}
    except zipfile.BadZipFile:
        # Handle bad zip files
        return {'error': 'Invalid zip file'}
    except Exception as e:
        # Handle any other exceptions
        return {'error': str(e)}

# Define an error view for internal server errors
@view_config(context=HTTPInternalServerError)
def internal_server_error(request):
    return {'error': 'Internal Server Error'}

# Define the configuration function for the Pyramid app
def main(global_config, **settings):
    config = Configurator(settings=settings)
    
    # Scan for @view_config decorators to setup routes
    config.scan()
    
    # Return the Pyramid WSGI app
    return config.make_wsgi_app()
