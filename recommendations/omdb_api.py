from django.shortcuts import render
from django.http import JsonResponse
import requests

API_KEY = 'your_omdb_api_key'
BASE_URL = 'http://www.omdbapi.com/'

def recommend_by_genre(request):
    genre = request.GET.get('genre')
    movies = []
    if genre:
        # Fetch movies based on genre
        response = requests.get(BASE_URL, params={'apikey': API_KEY, 's': genre})
        data = response.json()
        if data.get('Search'):
            for movie in data['Search']:
                movies.append({
                    'title': movie.get('Title', 'No Title'),
                    'poster': movie.get('Poster', 'https://via.placeholder.com/150')
                })
    return render(request, 'index.html', {'movies': movies})

def recommend_by_movie(request):
    movie = request.GET.get('movie')
    movies = []
    if movie:
        # Fetch similar movies
        response = requests.get(BASE_URL, params={'apikey': API_KEY, 't': movie})
        movie_data = response.json()
        if movie_data and 'Genre' in movie_data:
            genres = movie_data['Genre'].split(', ')[:3]  # Use top 3 genres
            for genre in genres:
                genre_response = requests.get(BASE_URL, params={'apikey': API_KEY, 's': genre})
                genre_data = genre_response.json()
                if genre_data.get('Search'):
                    for movie_item in genre_data['Search']:
                        movies.append({
                            'title': movie_item.get('Title', 'No Title'),
                            'poster': movie_item.get('Poster', 'https://via.placeholder.com/150')
                        })
    return render(request, 'index.html', {'movies': movies})
