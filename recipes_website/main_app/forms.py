from .models import Comment, Recipe
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        labels = {
            'name': 'Имя автора',
            'body': 'Комментарий'
        }

class SearchForm(forms.Form):
    query = forms.CharField(label= 'Введите запрос')

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_instructions', 'cooking_time']