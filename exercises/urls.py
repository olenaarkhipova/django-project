from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExerciseListView.as_view(), name="exercises-home"),
    path('exercise/<int:pk>/', views.ExerciseDetailView.as_view(), name="exercises-detail"),
    path('exercise/create/', views.ExerciseCreateView.as_view(), name="exercises-create"),
    path('exercise/<int:pk>/update/', views.ExerciseUpdateView.as_view(), name="exercises-update"),
    path('exercise/<int:pk>/delete/', views.ExerciseDeleteView.as_view(), name="exercises-delete"),
    path('about/', views.about, name="exercises-about"),
    path('search/', views.ExerciseSearchView.as_view(), name='exercise-search'),
    path('moderation/', views.ExerciseModerationView.as_view(), name='exercise-moderation'),
    path('approve/<int:pk>/', views.ExerciseApprovalView.as_view(), name='exercise-approval'),
    path('approval-success/<int:pk>/', views.ExerciseApprovalSuccessView.as_view(), name='exercise-approval-success'),
]
