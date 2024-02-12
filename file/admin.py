from django.contrib import admin

from file.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at', 'processed',)
    list_filter = ('processed',)
