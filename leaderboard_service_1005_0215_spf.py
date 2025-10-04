# 代码生成时间: 2025-10-05 02:15:25
# leaderboard_service.py

"""
This module provides a leaderboard service for storing and retrieving user scores.
"""
import re
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response


# Define a simple in-memory database for storing scores.
# In a real-world application, this would be replaced with a database.
class InMemoryDatabase:
    def __init__(self):
        self.scores = []

    def add_score(self, username, score):
        # Add a new score, ensuring the username does not exceed 20 characters.
        if len(username) > 20:
            raise ValueError("Username too long")
        self.scores.append((username, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)  # Sort scores in descending order.

    def get_top_scores(self, count=10):
        # Return the top 'count' scores.
        return self.scores[:count]

# Instantiate the in-memory database.
database = InMemoryDatabase()

# Define the Pyramid configuration function.
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Define the route for adding a score.
    config.add_route('add_score', '/add_score')
    config.scan()

    return config.make_wsgi_app()

# Define the view to add a score.
@view_config(route_name='add_score', renderer='json')
def add_score(request):
    """
    This view adds a new score to the leaderboard.
    """
    try:
        # Extract the username and score from the request.
        username = request.matchdict['username']
        score = int(request.matchdict['score'])
        # Add the score to the database.
        database.add_score(username, score)
        return {'status': 'success', 'message': 'Score added successfully'}
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        # Handle any other exceptions.
        return {'status': 'error', 'message': 'An unexpected error occurred'}

# Define the view to get the top scores.
@view_config(route_name='top_scores', renderer='json')
def top_scores(request):
    """
    This view returns the top scores from the leaderboard.
    """
    try:
        # Extract the count of top scores from the request.
        count = int(request.params.get('count', 10))
        # Retrieve the top scores from the database.
        top_scores = database.get_top_scores(count)
        return {'status': 'success', 'message': 'Top scores retrieved successfully', 'scores': top_scores}
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        # Handle any other exceptions.
        return {'status': 'error', 'message': 'An unexpected error occurred'}
