from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Recipe.Status.PUBLISHED)

def recipe_image_directory_path(instance: "Recipe", filename: str) -> str:
    return "recipes/recipe_{pk}/image/{filename}".format(
        pk=instance.pk,
        filename=filename
    )

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


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
    image = models.ImageField(null=True, blank=True, upload_to=recipe_image_directory_path)
    categories = models.ManyToManyField(Category, blank=True)

    objects = models.Manager()
    published_recipes = PublishedManager()

    # image =

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'])
        ]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main_app:recipe_detail', args=[self.slug,
                                                       self.published.year,
                                                       self.published.month,
                                                       self.published.day])

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment {self.name} on {self.recipe}'