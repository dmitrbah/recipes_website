from django.contrib import admin
from .models import Recipe, Comment, Category

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'author', 'published', 'status']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['status', 'created', 'published', 'author']
    search_fields = ['name', 'description']
    raw_id_fields = ['author']
    date_hierarchy = 'published'
    ordering = ['status', 'published']
    filter_horizontal = ['categories']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'name', 'body', 'active', ]
    list_filter = ['active', 'created', 'updated', ]
    search_fields = ['name', 'body']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
