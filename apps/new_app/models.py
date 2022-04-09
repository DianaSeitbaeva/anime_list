from datetime import datetime
import email
from enum import unique
from tabnanny import verbose
from django.db import models
from auths.models import CustomUser
from django.core.exceptions import ValidationError
from abstracts.models import AbstractDateTime
from django.db.models import QuerySet


class Group(AbstractDateTime):
    GROUP_NAME_MAX_LENGTH = 10
    name = models.CharField(
        max_length=GROUP_NAME_MAX_LENGTH
    )
    #objects = GroupQuerySet().as_manager()

    def __str__(self) -> str:
        return f'Group: {self.name}' 

    
    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class StudentQuerySet(QuerySet):
    ADULT_AGE = 18
    HIGH_GPA_LEVEL = 4.0

    def get_adult_students(self) -> QuerySet:
        return self.filter(
            age__gte=self.ADULT_AGE
        )


class Student(AbstractDateTime):
    MAX_AGE = 27
    #один аккаунт = много студентов

    account=models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE)

    age=models.IntegerField(
        'Возраст студента')

    group=models.ForeignKey(
        Group, on_delete=models.PROTECT
    )
    GPA=models.FloatField(
        'Средний значение GPA'
    )
    objects = StudentQuerySet().as_manager()

    def __str__(self) -> str:
        return f'Student: {self.account}, Age: {self.age}, group: {self.group}, GPA: {self.GPA}' 


    def save(
        self,
        *args: tuple,
        **kwargs: dict
    ) -> None:
        if self.age > self.MAX_AGE:
            raise ValidationError(
                f'Допустимый возраст: {self.MAX_AGE}'
            )
            #self.age = self.MAX_AGE
        super().save(*args, **kwargs)

    def delete(self) -> None:
        breakpoint()
        datetime_now: datetime = datetime.now()

        self.datetime_deleted = datetime_now

        self.save(
            update_fields = ['datetime_deleted']
        )
    
    class Meta:
        ordering = (
            'account',
            'age',
            'group',
            'GPA',
        )
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Professor(AbstractDateTime):
    FULL_NAME_MAX_LENGTH = 20

    TOPIC_JAVA = 'java'
    TOPIC_PYTHON = 'python'
    TOPIC_TS = 'typescript'
    TOPIC_JS = 'javascript'
    TOPIC_RUBY = 'ruby'
    TOPIC_GO = 'golang'
    TOPIC_SQL = 'sql'
    TOPIC_SWIFT = 'swift'
    TOPIC_PHP = 'php'
    TOPIC_DELPHI = 'delphi'
    TOPIC_PERL = 'perl'

    TOPIC_CHOICES = (
        (TOPIC_JAVA,'Java'),
        (TOPIC_PYTHON,'Python'),
        (TOPIC_TS,'TypeScript'),
        (TOPIC_JS,'JavaScript'),
        (TOPIC_RUBY,'Ruby'),
        (TOPIC_GO,'Golang'),
        (TOPIC_SQL,'SQL'),
        (TOPIC_SWIFT,'Swift'),
        (TOPIC_PHP,'PHP'),
        (TOPIC_DELPHI,'Delphi'),
        (TOPIC_PERL,'Perl'),
    )

    full_name = models.CharField(
        verbose_name='полное имя', 
        max_length=FULL_NAME_MAX_LENGTH)
    topic = models.CharField(
        verbose_name='предмет',
        choices=TOPIC_CHOICES,
        default=TOPIC_PYTHON,
        max_length=FULL_NAME_MAX_LENGTH
    )
    students = models.ManyToManyField(
        Student
    )

    def __str__(self) -> str:
        return f'Professor: {self.full_name}, Topic: {self.topic}' 

    def save(
        self,
        *args: tuple,
        **kwargs: dict
    ) -> None:
        if self.full_name.__len__() > self.FULL_NAME_MAX_LENGTH:
            raise ValidationError(
                f'Допустимая длинна имени: {self.FULL_NAME_MAX_LENGTH}'
            )
            #self.age = self.MAX_AGE
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = (
            'full_name',
            'topic',
        )
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class FileQuerySet(models.QuerySet):
    def get_is_checked(self) -> models.QuerySet:
        return self.filter(
            homework__is_checked = True
        )


class HomeworkQuerySet(QuerySet):
    def get_not_deleted(self) -> QuerySet:
        return self.filter(
            datetime_deleted__isnull=True
        )


class Homework(AbstractDateTime):
    title = models.CharField(
        max_length=35,
    ) 
    subject = models.CharField(
        max_length=35,
    ) 
    logo = models.ImageField(
        upload_to='%d.%m.%Y',
    )
    homework = models.ForeignKey(
        'File', 
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
    )

    objects = HomeworkQuerySet.as_manager()

    @property
    def is_checked(self) -> bool:
        return all(
            self.files.values_list(
                'is_checked', flat=True
            )
        )

class File(AbstractDateTime):
    FILE_TYPES = (
        'txt',
        'pdf',
    )
    homework = models.ForeignKey(
        Homework,
        verbose_name='домашняя работа',
        related_name='files',
        on_delete=models.PROTECT
    )
    title = models.CharField(
        verbose_name='заголовок',
        max_length=100,
    )
    obj = models.FileField(
        upload_to='homework_files/%Y/%m/%d',
        max_length=255,
    )
    is_checked = models.BooleanField(
        verbose_name='проверен ли',
        default=False
    )
    objects = FileQuerySet.as_manager()

    def __str__(self) -> str:
        return f'{self.homework.title}'

    class Meta:
        ordering = {
            '-datetime_created',
        }
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'