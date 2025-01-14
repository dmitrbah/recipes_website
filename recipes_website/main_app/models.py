from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Recipe.Status.PUBLISHED)


class Recipe(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recipes')
    description = models.CharField(max_length=200)
    cooking_instructions = models.TextField()
    cooking_time = models.CharField(max_length=30, blank=True, null=True)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published_recipes = PublishedManager()

    # image =
    # author =

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'])
        ]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('main_app:recipe_detail', args=[self.slug,
                                                       self.published.year,
                                                       self.published.month,
                                                       self.published.day])
