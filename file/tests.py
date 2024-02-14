from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from file.models import File
from file.tasks import file_treatment


class FileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.file = File.objects.create(
            file='test.txt',
            uploaded_at=datetime.now(),
            processed=False
        )

    def test_file_treatment(self):
        file_treatment(file_id=self.file.id)
        self.file.refresh_from_db()
        self.assertTrue(self.file.processed)

    def test_list_view(self):
        response = self.client.get(reverse('file:files_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_upload_txt_view(self):
        test_file = SimpleUploadedFile(name='test1.txt', content=b'test', content_type='text/plain')
        response = self.client.post(
            reverse('file:file_upload'),
            {'file': test_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 2)

    def test_upload_jpg_view(self):
        test_file = SimpleUploadedFile(name='test1.jpg', content=b'test', content_type='image/jpeg')
        response = self.client.post(
            reverse('file:file_upload'),
            {'file': test_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 2)

    def test_upload_wrong_view(self):
        test_file = SimpleUploadedFile(name='test1.zip', content=b'test', content_type='text/plain')
        response = self.client.post(
            reverse('file:file_upload'),
            {'file': test_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(File.objects.count(), 1)
