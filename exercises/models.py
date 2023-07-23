from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Exercise(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='exercise_photos/', blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    def get_absolute_url(self):
        return reverse("exercises-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
