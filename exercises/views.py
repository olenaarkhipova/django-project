from django.core.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


from . import models
from .forms import ExerciseForm, ExerciseSearchForm
from .models import Exercise

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

    def get_queryset(self):
        return models.Exercise.objects.filter(is_approved=True)


class ExerciseDetailView(DetailView):
    model = models.Exercise


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = models.Exercise
    form_class = ExerciseForm
    template_name = 'exercises/exercise_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_approved = False
        return super().form_valid(form)


class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Exercise
    form_class = ExerciseForm
    template_name = 'exercises/exercise_form.html'

    def test_func(self):
        exercise = self.get_object()
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user == exercise.author

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            raise PermissionDenied("You do not have the required permissions.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.user.is_superuser or self.request.user.is_staff:
            form.instance.is_approved = True  # Approve the exercise if admin user updates it
        form.instance.status = 'pending'
        return super().form_valid(form)


class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Exercise
    success_url = reverse_lazy('exercises-home')

    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.author


class ExerciseSearchView(View):
    template_name = 'exercises/search_results.html'

    def get(self, request):
        form = ExerciseSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Exercise.objects.filter(title__icontains=query)
        else:
            results = Exercise.objects.none()

        context = {
            'form': form,
            'results': results,
        }
        return render(request, self.template_name, context)


class ExerciseModerationView(ListView):
    model = models.Exercise
    template_name = 'exercises/exercise_moderation.html'
    context_object_name = 'exercises'

    @method_decorator(user_passes_test(lambda u: u.is_superuser or u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return models.Exercise.objects.filter(is_approved=False, status='pending')


class ExerciseApprovalView(View):
    def post(self, request, pk):
        exercise = get_object_or_404(models.Exercise, pk=pk)

        if not request.user.is_superuser and not request.user.is_staff:
            # Only admin users can approve/reject exercises
            return redirect('exercises-home')

        if 'approve' in request.POST:
            exercise.status = 'approved'
            exercise.is_approved = True
            exercise.save()
            return redirect(reverse('exercise-approval-success', args=[pk]))
        elif 'reject' in request.POST:
            exercise.status = 'rejected'
            exercise.is_approved = False
            exercise.save()

        return redirect('exercise-moderation')


class ExerciseApprovalSuccessView(View):
    def get(self, request, pk):
        exercise = get_object_or_404(models.Exercise, pk=pk)
        return render(request, 'exercises/exercise_approval_success.html', {'exercise': exercise})


def about(request):
    return render(request, "exercises/about.html", {'title': 'about us page'})
