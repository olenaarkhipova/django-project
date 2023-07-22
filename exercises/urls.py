from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExerciseListView.as_view(), name="exercises-home"),
    path('exercise/<int:pk>/', views.ExerciseDetailView.as_view(), name="exercises-detail"),
    path('exercise/create/', views.ExerciseCreateView.as_view(), name="exercises-create"),
    path('exercise/<int:pk>/update/', views.ExerciseUpdateView.as_view(), name="exercises-update"),
    path('exercise/<int:pk>/delete/', views.ExerciseDeleteView.as_view(), name="exercises-delete"),
    path('about/', views.about, name="exercises-about"),
]
