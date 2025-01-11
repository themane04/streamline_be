from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    profile_image = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default_avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
