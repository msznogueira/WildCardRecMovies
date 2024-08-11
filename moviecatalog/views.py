from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from moviecatalog.models import Movie, Genre, Director, Actor, SearchTerm, MovieSearchTerm
from moviecatalog.serializer import MovieSerializer, GenreSerializer, DirectorSerializer, ActorSerializer
import os

class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ActorsViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class DirectorsViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class MovieSearchView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        search_term_query = self.request.query_params.get('search_term')
        if search_term_query is None:
            return Movie.objects.none()  # Return an empty queryset

        search_term, created = SearchTerm.objects.get_or_create(term=search_term_query)
        movies = Movie.objects.filter(moviesearchterm__search_term=search_term)

        if movies.exists():
            return movies
        
        # Fetch from external API if no movies are found
        self.fetch_movies_from_external_api(search_term_query, search_term)
        return Movie.objects.filter(moviesearchterm__search_term=search_term)

    def fetch_movies_from_external_api(self, search_term_query, search_term):
        response = requests.get(
            'https://api.themoviedb.org/3/search/movie', 
            params={
                'query': search_term_query, 
                'api_key': os.getenv("TMDB_API_KEY"),
            }
        )
        if response.status_code == 200:
            movies_data = response.json()
            for movie_dict in movies_data['results']:
                try:
                    movie, _ = Movie.objects.get_or_create(
                        title=movie_dict['title'],
                        defaults={
                            'overview': movie_dict['overview'],
                            'release_date': movie_dict['release_date'],
                            # other fields
                        }
                    )
                    MovieSearchTerm.objects.get_or_create(movie=movie, search_term=search_term)
                except ValidationError as e:
                    print(e)
        else:
            raise ValueError(f"Failed to fetch data from external API: {response.status_code}")

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response({"error": "Search term is empty"}, status=400)
        return super().list(request, *args, **kwargs)

