from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField()
    poster_path = models.CharField()
    vote_average = models.FloatField()
    is_watchlisted = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'
