from datetime import datetime

from django.db.models import (
    Model,
    ManyToManyField,
    OneToOneField,
    CharField,
    TextField,
    IntegerField,
    DateTimeField,
)
from abstracts.models import AbstractDateTime


class Genre(Model):
    """Genre entity."""

    name = CharField(
        verbose_name='имя',
        max_length=50
    )


class Description(Model):
    """Description entity."""

    text_en = TextField(
        verbose_name='текст на английском'
    )
    text_ru = TextField(
        verbose_name='текст на русском'
    )


class Title(Model):
    """Title entity."""

    name = CharField(
        verbose_name='имя',
        max_length=50
    )
    link = TextField(
        verbose_name='ссылка'
    )


class ReleaseDate(Model):
    """ReleaseDate entity."""

    published = CharField(
        verbose_name='имя',
        max_length=20
    )
    date = DateTimeField(
        verbose_name='дата'
    )


class Anime(AbstractDateTime):
    """Anime entity."""

    studio = CharField(
        verbose_name='студия',
        max_length=100,
    )
    genre = ManyToManyField(
        Genre,
        verbose_name='жанры',
        on_delete=models.PROTECT
    )
    rating = IntegerField(
        verbose_name='рейтинг',
    )
    description = OneToOneField(
        Description,
        verbose_name='описание',
        on_delete=models.PROTECT
    )
    title = OneToOneField(
        Title,
        verbose_name='название', 
        on_delete=models.CASCADE
    )
    start_date = OneToOneField(
        ReleaseDate,
        verbose_name='дата выпуска',
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = (
            '-datetime_created'
        )
        verbose_name = 'аниме'
        verbose_name_plural = 'аниме'

    def __str__(self) -> str:
        return f'{self.studio} | {self.title.name}, {self.rating}'

    def save(self, *args: tuple, **kwargs: dict) -> None:
        pass
        # super().save(*args, **kwargs)

    def delete(self) -> None:
        self.datetime_deleted = datetime.now()
        self.save(
            update_field=['datetime_deleted']
        )
        # super().delete()