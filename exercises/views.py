from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from . import models

# Create your views here.


def home(request):
    exercises = models.Exercise.objects.all()
    context = {
        'exercises': exercises
    }
    return render(request, "exercises/home.html", context)


class ExerciseListView(ListView):
    model = models.Exercise
    template_name = 'exercises/home.html'
    context_object_name = 'exercises'


class ExerciseDetailView(DetailView):
    model = models.Exercise


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = models.Exercise
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Exercise
    fields = ['title', 'description']

    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Exercise
    success_url = reverse_lazy('exercises-home')

    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.author


def about(request):
    return render(request, "exercises/about.html", {'title': 'about us page'})
