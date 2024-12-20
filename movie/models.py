from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField()
    poster_path = models.CharField()
    vote_average = models.FloatField()

    @property
    def full_poster_path(self):
        return f"https://image.tmdb.org/t/p/w500{self.poster_path}"

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'
