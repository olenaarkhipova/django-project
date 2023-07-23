from django import forms
from .models import Exercise


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'description', 'photo']


class ExerciseSearchForm(forms.Form):
    query = forms.CharField(max_length=100)
