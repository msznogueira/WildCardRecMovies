from rest_framework import serializers
from moviecatalog.models import Movie, Genre, Director, Actor, SearchTerm, MovieSearchTerm

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerm
        fields = ['term']
