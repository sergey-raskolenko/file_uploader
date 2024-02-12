from django.urls import path
from file.apps import FileConfig
from file.views import FileUploadView, FileListView

app_name = FileConfig.name

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('files/', FileListView.as_view(), name='files_list'),
]
