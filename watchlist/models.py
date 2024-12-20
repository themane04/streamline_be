from django.db import models


class Watchlist(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField()
    poster_path = models.CharField()
    vote_average = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'watchlist'
