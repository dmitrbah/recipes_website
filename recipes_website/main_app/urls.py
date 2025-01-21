from django.urls import path
from . import views
from .views import RecipeUpdateView, RecipeDeleteView

app_name = 'main_app'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<slug:recipe>/<int:year>/<int:month>/<int:day>/', views.recipe_detail, name='recipe_detail'),
    path('<int:pk>/update', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:pk>/delete', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('<int:post_id>/comment', views.post_comment, name='post_comment'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('add_recipe/', views.add_recipe, name='add_recipe')
]