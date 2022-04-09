from dataclasses import fields
from multiprocessing import context
from pyexpat import model
from re import template
from unittest import loader
from wsgiref.simple_server import WSGIRequestHandler
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm
)
from django.http import HttpResponse
from django.shortcuts import render
from auths.models import CustomUser
from new_app.models import Homework
from apps.abstracts.handlers import ViewHandler
from django.views import View
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'email',
        )


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = (
            'email',
        )


class CreateHomeworkView(ViewHandler, View):

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:

        if not request.user.is_authentificated:
            return render(
                request,
                'login.html'
            )

        form: HomeworkForm = HomeworkForm(
            request.POST or None,
            request.FILES or None
        )

        if not form.is_valid():
            context: dict = {
                'ctx_form': form,
            }
            template_name = loader.get_template(
                'homework_create.html'
            )
            return HttpResponse(
                template_name.render(
                    context,
                    request
                ),
                context_type='text/html'
            )
        homework = form.save(commit=False)
        homework.user = request.user
        homework.logo = request.FILES['logo']
        file_type = homework_pk.logo.urls.split('.')[-1].lower()
        file_type = file_type.lower()

        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'homework': homework,
                'form': form,
                'error_message': 'PNG, JPG, JPEG'
            }
            return render(
                request,
                'create_album.html',
                context
            )
        homework.save()
        return render(
            request,
            'detail.html',
            {'homework': homework}
        )