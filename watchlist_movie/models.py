from django.db import models


class WatchlistMovie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField()
    poster_path = models.CharField()
    vote_average = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'watchlist_movies'
