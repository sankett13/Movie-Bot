from django.shortcuts import render
from justwatch import JustWatch

# Initialize JustWatch API for India (use country='IN')
justwatch_api = JustWatch(country='IN')

def index(request):
    return render(request, 'index.html')

import requests
from django.shortcuts import render
from django.http import JsonResponse
from .omdb_api import recommend_by_genre, recommend_by_movie

API_KEY = 'f354aa4'  # Your OMDb API key
BASE_URL = 'http://www.omdbapi.com/'

def recommend_by_genre(request):
    genre = request.GET.get('genre')  # Get genre from the GET parameters
    movies = []

    if genre:
        page = 1  # Initialize page number for pagination
        while len(movies) < 10:  # Try to fetch up to 20 movies
            # Perform a search with a genre-related keyword (e.g., "action")
            response = requests.get(BASE_URL, params={'apikey': API_KEY, 's': genre, 'page': page})
            data = response.json()

            # Check if the response contains movie results
            if data.get('Search'):
                for movie in data['Search']:
                    # Fetch detailed information about the movie
                    movie_details = requests.get(BASE_URL, params={'apikey': API_KEY, 't': movie['Title']}).json()
                    # Check if genre info is available in the movie's details
                    movie_genres = movie_details.get('Genre', '').split(', ')  # Split genres by comma
                    if genre.lower() in [g.lower() for g in movie_genres]:  # Check if genre matches
                        movies.append({
                            'title': movie.get('Title', 'No Title'),
                            'poster': movie.get('Poster', 'https://via.placeholder.com/150')
                        })
            else:
                print(f"Error: {data.get('Error', 'No movies found')}")
                break  # Exit loop if no movies found or API error occurs
            
            page += 1  # Increment the page number to fetch the next page of results if needed

    return render(request, 'index.html', {'movies': movies})



def recommend_by_movie(request):
    """
    Fetch and return similar movies based on a given movie title using OMDb API.
    """
    movie_title = request.GET.get('movie')
    movies = []

    if movie_title:
        try:
            # Search for a movie by title using OMDb API
            response = requests.get(BASE_URL, params={'apikey': API_KEY, 't': movie_title})
            movie_data = response.json()

            # If the movie data is found and has a Genre field
            if movie_data and 'Genre' in movie_data:
                genres = movie_data['Genre'].split(', ')[:3]  # Use top 3 genres to fetch similar movies

                # Fetch similar movies by genre
                for genre in genres:
                    genre_response = requests.get(BASE_URL, params={'apikey': API_KEY, 's': genre})
                    genre_data = genre_response.json()
                    if genre_data.get('Search'):
                        for movie_item in genre_data['Search']:
                            movies.append({
                                'title': movie_item.get('Title', 'No Title'),
                                'poster': movie_item.get('Poster', 'https://via.placeholder.com/150'),
                                'year': movie_item.get('Year', 'N/A')
                            })
        except Exception as e:
            print(f"Error fetching movie recommendations: {e}")
            return JsonResponse({'error': 'Failed to fetch data from OMDb API'}, status=500)

    return render(request, 'index.html', {'movies': movies})
