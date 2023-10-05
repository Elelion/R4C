from django.db import models
from django.core import validators


def validate_two_characters(value):
    if len(value) != 2:
        raise validators.ValidationError("Должно быть два символа")


class Robot(models.Model):
    serial = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        unique=True)

    model = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        validators=[validate_two_characters])

    version = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        validators=[validate_two_characters])

    created = models.DateTimeField(
        blank=False,
        null=False)

    available = models.BooleanField(
        default=True)

    quantity = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False)