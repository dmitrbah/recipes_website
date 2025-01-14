from django.shortcuts import render, get_object_or_404
from .models import Recipe

def recipe_list(request):
    recipes = Recipe.published_recipes.all()
    return render(request, 'main_app/list.html', {'recipes': recipes})

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id, status=Recipe.Status.PUBLISHED)
    return render(request, 'main_app/recipe_detail.html', {'recipe': recipe})
