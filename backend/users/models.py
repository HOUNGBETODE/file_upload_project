import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator


def validate_user_genre(value):
    allowed_values = [choice[0] for choice in UserGenre.choices]  # Extract allowed values
    if value not in allowed_values:
        raise ValidationError('Invalid user genre. Choose from {}'.format(', '.join(allowed_values)))


class UserGenre(models.TextChoices):
    MALE = 'mal'
    FEMALE = 'fem'


class User(AbstractUser):
    # fields username and email
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=10, blank=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    # setting up a field for genre stuff
    genre = models.CharField(max_length=3, choices=UserGenre.choices, validators=[validate_user_genre])
    # overwritting standard USERNAME and EMAIL FIELDS
    USERNAME_FIELD = 'username'
    EMAIL_FIELD= 'email'

    REQUIRED_FIELDS = ['email', 'genre']
