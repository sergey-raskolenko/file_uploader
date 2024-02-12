from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from file.models import File
from file.serializers import FileListSerializer, FileUploadSerializer
from file.tasks import file_treatment


class FileUploadView(CreateAPIView):
    """Контроллер для загрузки файлов"""
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_treatment(file_id=serializer.instance.id)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FileListView(ListAPIView):
    """Контроллер для получения списка файлов"""
    queryset = File.objects.all()
    serializer_class = FileListSerializer
