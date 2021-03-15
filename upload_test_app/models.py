from django.db import models

# Create your models here.

from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='upload_test_app/')
    uploaded_at = models.DateTimeField(auto_now_add=True)