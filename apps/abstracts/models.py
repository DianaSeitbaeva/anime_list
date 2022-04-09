from django.db import models

class AbstractDateTime(models.Model):
    datetime_created=models.DateTimeField(
        verbose_name='время создания',
        auto_now=True
        )
    datetime_updated=models.DateTimeField(
        verbose_name='время обновления',
        auto_now=True)
    datetime_deleted=models.DateTimeField(
        verbose_name='время удаления',
        null=True,
        blank=True)

    class Meta():
        abstract = True

    def __str__(self) -> str:
        return f'время создания: {self.datetime_created}, время изменения: {self.datetime_updated}, время удаления: {self.datetime_deleted}'
