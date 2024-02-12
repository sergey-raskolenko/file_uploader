from django.contrib import admin

from file.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_filter = ('processed',)
