# 代码生成时间: 2025-10-03 02:04:27
# neural_network_visualization.py

"""
This module provides functionality for visualizing neural networks. It is designed to be
used with the Pyramid framework to create a web application that can display neural networks.
"""

from pyramid.view import view_config
from pyramid.response import Response
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import ChameleonFormRenderer
from pyramid.renderers import render_to_response
import matplotlib.pyplot as plt
from tensorflow.keras.utils import plot_model


class NeuralNetworkVisualizationForm(Form):
    """Form for collecting neural network visualization data."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer = ChameleonFormRenderer()
        self.fieldsets = [
            ('Neural Network', {'fields': ['model_path']}),
        ]
        self.fields['model_path'] = 'text'
        self.fields['model_path'].required = True
        self.fields['model_path'].validator = self.validate_model_path

    def validate_model_path(self, field):
        """Validate the model path."""
        if not field.value or not field.value.endswith('.h5'):
            raise ValueError('Invalid model path. Please provide a valid .h5 file.')
        return True


@view_config(route_name='visualize_neural_network', renderer='templates/neural_network_visualization.pt')
def visualize_neural_network(request):
    """
    Route handler for visualizing a neural network.
    
    This function handles the GET request and renders the form template.
    If the form is submitted with a valid model path, it uses
    TensorFlow's plot_model function to generate a graphical representation
    of the neural network.
    """
    form = NeuralNetworkVisualizationForm(request.POST, request)
    if request.method == 'POST' and form.validate():
        model_path = form.model_path.value
        try:
            # Load the model
            from tensorflow.keras.models import load_model
            model = load_model(model_path)
            
            # Plot the model
            plot_model(model, to_file='/tmp/model_visualization.png', show_shapes=False, show_layer_names=True)
            
            # Render the visualization in the response
            response = Response(content_type='image/png')
            response.body = plt.imread('/tmp/model_visualization.png').tobytes()
            return response
        except Exception as e:
            return Response('Error: ' + str(e), content_type='text/plain')
    else:
        return render_to_response('neural_network_visualization.pt', {'form': form}, request)
