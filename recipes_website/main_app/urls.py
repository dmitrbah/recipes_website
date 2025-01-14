from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<slug:recipe>/<int:year>/<int:month>/<int:day>/', views.recipe_detail, name='recipe_detail'),
    path('<int:post_id>/comment', views.post_comment, name='post_comment')
]