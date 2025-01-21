from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from .models import Recipe, Comment
from .forms import CommentForm, SearchForm, RecipeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import UpdateView, DeleteView

def recipe_list(request):
    recipe_list = Recipe.published_recipes.all()
    for recipe in recipe_list:
        recipe.save()
    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    return render(request, 'main_app/list.html', {'recipes': recipes})

def recipe_detail(request, recipe, year, month, day):
    recipe = get_object_or_404(Recipe,
                               status=Recipe.Status.PUBLISHED,
                               slug=recipe,
                               published__year=year,
                               published__month=month,
                               published__day=day)
    comments = recipe.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'main_app/recipe_detail.html', {'recipe': recipe,
                                                           'comments': comments,
                                                           'form': form})


@require_POST
def post_comment(request, post_id):
    recipe = get_object_or_404(Recipe,
                               id=post_id,
                               status=Recipe.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.save()
    return render(request, 'main_app/comment.html', {'recipe': recipe,
                                                     'form': form,
                                                     'comment': comment})

def recipe_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('name', 'description', 'cooking_instructions', config='russian')
            search_query = SearchQuery(query, config='russian')
            results = Recipe.published_recipes.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')

    return render(request, 'main_app/search.html',
                  {'form': form, 'query': query, 'results': results})

def add_recipe(request):
    if request.method == 'POST':
        recipe = None
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.status = Recipe.Status.PUBLISHED
            recipe.save()
            return HttpResponseRedirect('/')
    form = RecipeForm()
    return render(request, 'main_app/add_recipe.html', {'form': form})


class RecipeUpdateView(UpdateView):
    model = Recipe
    fields = ['name', 'description', 'cooking_instructions', 'cooking_time', 'image', 'categories']
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return Recipe.get_absolute_url(self.object)


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy("main_app:recipe_list")

