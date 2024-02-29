from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from moviecatalog.models import Movie, Genre, Director, Actor, SearchTerm, MovieSearchTerm
from moviecatalog.serializer import MovieSerializer, GenreSerializer, DirectorSerializer, ActorSerializer, SearchTermSerializer
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

class MovieSearchView(APIView):

    def get(self, request):
        # headers = {
        #     "accept": "application/json",
        #     "Authorization": "Bearer " + os.getenv("TMDB_API_KEY")
        # }        
        search_term_query = request.query_params.get('search_term')
        if search_term_query == None:
            return Response({"error": "Search term is empty"})
        search_term, created = SearchTerm.objects.get_or_create(search_term=search_term_query)

        if not created:
            movies = Movie.objects.filter(moviesearchterm__search_term=search_term_query)
            serializer = SearchTermSerializer()
            return Response(serializer.data)
        else:
            # Call external API and process response as before
            response = requests.get('https://api.themoviedb.org/3/search/movie', 
                                    params={
                                        'query': search_term_query, 
                                        'api_key': os.getenv("TMDB_API_KEY"),
                                            })
            if response.status_code == 200:
                movie_data = response.json()
                for movie_dict in movie_data:
                    movie, _ = Movie.objects.get_or_create(
                        title=movie_dict['title'],
                        defaults={
                            'description': movie_dict['description'],
                            'release_date': movie_dict['release_date'],
                            # other fields
                        }
                    )
                    MovieSearchTerm.objects.create(movie=movie, search_term=search_term)
                movies = Movie.objects.filter(moviesearchterm__search_term=search_term)
                serializer = MovieSerializer(movies, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "Failed to fetch data from external API"}, status=response.status_code)

