from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from config import settings
from file.models import File
from file.serializers import FileListSerializer, FileUploadSerializer
from file.tasks import file_treatment
from pathlib import Path


class FileUploadView(CreateAPIView):
    """Контроллер для загрузки файлов"""
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_format = Path(request.FILES['file']._name).suffix
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if file_format in settings.ALLOWED_IMAGE_FORMATS:
                file = serializer.save()
                file_treatment.delay(file_id=file.id)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            elif file_format in settings.ALLOWED_DOCUMENT_FORMATS:
                file = serializer.save()
                file_treatment.delay(file_id=file.id)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.data,
                    status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FileListView(ListAPIView):
    """Контроллер для получения списка файлов"""
    queryset = File.objects.all()
    serializer_class = FileListSerializer
