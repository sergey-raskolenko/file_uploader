from django.db import models


class File(models.Model):
    """
    Модель для описания файлов
    """
    file = models.FileField(
        upload_to='files/', unique=True, verbose_name='Файл'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата загрузки'
    )
    processed = models.BooleanField(
        default=False, verbose_name='Статус обработки'
    )

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
        db_table = 'file'

    def __str__(self):
        return f'{self.file}: {self.uploaded_at}'

    def __repr__(self):
        return f'File({self.file}, {self.uploaded_at}, {self.processed})'
