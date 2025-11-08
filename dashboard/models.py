from django.db import models
from django.contrib.auth.models import User
import os

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    status = models.BooleanField(max_length=20, default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scan_result = models.CharField(max_length=255, default="Not Scanned")
    file_hash = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.file.name


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} @ {self.timestamp:%Y-%m-%d %H:%M:%S}"
