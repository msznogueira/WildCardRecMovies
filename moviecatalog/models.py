from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=True)
    director = models.ForeignKey('Director', on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField('Actor', related_name='movies')
    description = models.TextField(null=True)
    year = models.IntegerField(null=True)   
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    
class SearchTerm(models.Model):
    search_term = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.search_term

class MovieSearchTerm(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    search_term = models.ForeignKey(SearchTerm, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('movie', 'search_term')



