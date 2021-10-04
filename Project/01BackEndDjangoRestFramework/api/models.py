from enum import unique
import numpy as np
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Movie(models.Model):

    title = models.CharField(max_length=32, verbose_name="Movies title")
    description = models.CharField(max_length=360, verbose_name="Movies description")

    def number_ratings(self):
        ratings = Rating.objects.filter(movie = self)
        return ratings.count()

    def averege_ratings(self):


        ratings = Rating.objects.filter(movie = self)

        if ratings.count() > 0:

            sum_ratings = sum(np.array(ratings.values_list("stars", flat = True)))
            averege = sum_ratings/ratings.count()

        else:
            averege = 0

        return averege

class Rating(models.Model):

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),
    MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)