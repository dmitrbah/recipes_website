from django.shortcuts import render, get_object_or_404
from .models import Recipe

def recipe_list(request):
    recipes = Recipe.published_recipes.all()
    return render(request, 'main_app/list.html', {'recipes': recipes})

def recipe_detail(request, recipe, year, month, day):
    recipe = get_object_or_404(Recipe,
                               status=Recipe.Status.PUBLISHED,
                               slug=recipe,
                               published__year=year,
                               published__month=month,
                               published__day=day)
    return render(request, 'main_app/recipe_detail.html', {'recipe': recipe})
