from django.contrib import admin
from .models import UploadedFile, ActivityLog

admin.site.register(UploadedFile)
admin.site.register(ActivityLog)
