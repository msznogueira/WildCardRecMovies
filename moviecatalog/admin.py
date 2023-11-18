from django.contrib import admin
from moviecatalog.models import Movie, Genre, Director, Actor

class Movies(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_per_page = 20

class Genres(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Directors(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Actors(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Movie, Movies)
admin.site.register(Genre, Genres)
admin.site.register(Director, Directors)
admin.site.register(Actor, Actors)
