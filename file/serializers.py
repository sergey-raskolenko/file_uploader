from rest_framework import serializers
from file.models import File


class FileUploadSerializer(serializers.ModelSerializer):
    """Сериализатор для загрузки файлов"""
    class Meta:
        model = File
        fields = ('file',)


class FileListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка файлов"""
    class Meta:
        model = File
        fields = ('file', 'uploaded_at', 'processed')
        read_only_fields = ('file', 'uploaded_at', 'processed')
