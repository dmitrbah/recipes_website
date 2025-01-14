from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Recipe(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    name = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recipes')
    description = models.CharField(max_length=200)
    cooking_instruction = models.TextField()
    cooking_time = models.CharField(max_length=10, blank=True, null=True)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    # image =
    # author =

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'])
        ]

    def __str__(self):
        return f"{self.name}"
