from http.client import HTTPResponse
from multiprocessing import context
from typing import Optional
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.template import loader
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)
from django.db.models import (
    QuerySet,
    Q,
)
from django.views import View
from auths.forms import CustomUserChangeForm
from abstracts.handlers import (
    ViewHandler,
)
from new_app.models import (
    Homework,
)
from new_app.forms import (
    HomeworkForm,
)
    

class IndexView(ViewHandler, View):
    """Index View."""

    queryset: QuerySet = Homework.objects.get_not_deleted()
    template_name: str = 'index.html'

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """GET request handler."""

        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        homeworks: QuerySet = self.queryset.filter(
            user=request.user
        )
        query: str = request.GET.get('q')
        if query:
            homeworks = homeworks.filter(
                Q(titleicontains=query) | Q(subjecticontains=query)
            ).distinct()

        if not homeworks:
            homeworks = self.queryset

        context: dict = {
            'ctx_title': 'Главная страница',
            'ctx_homeworks': homeworks,
        }
        return self.get_http_response(
            request,
            self.template_name,
            context
        )

from new_app.models import (
    # Account, 
    Student,
    File,
    Homework,
)


from auths.models import (
    CustomUser,
)


def admin(request: WSGIRequest) -> HttpResponse:
    users: QuerySet = CustomUser.objects.all()
    context: dict = {
        'ctx_title': 'Главная страница',
        'ctx_users' : users,
    }
    return render(
        request,
        'admin.html',
        context,
    )


def show(request: WSGIRequest, username: str) -> HttpResponse:
    users: QuerySet = CustomUser.objects.get(
        username=username
    )
    context: dict = {
        'ctx_title': 'Профиль пользователя',
        'ctx_users' : users,
    }
    return render(
        request,
        template_name='show.html',
        context=context,
    )


class LoginView(View):

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ):
        if request.method == 'POST':
            email: str = request.POST['email']
            password: str = request.POST['password']

            user: CustomUser = dj_authenticate(
                email=email,
                password=password
            )
            
            
            if not user:
                return render(
                    request,
                    'login.html',
                    {'error_message': 'Невереные данные'}
                )
            if not user.is_active:
                return render(
                    request,
                    'login.html',
                    {'error_message': 'Ваш аккаунт был удален'}
                )
            dj_login(request, user)

            homeworks: QuerySet = Homework.objects.filter(
                user=request.user
            )
            return render(
                request,
                'index.html',
                {'homeworks': homeworks}
            )
        return render(
            request,
            'login.html'
        )


class LogoutView(View):
    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ):
        dj_logout(request)

        form: CustomUserChangeForm = CustomUserChangeForm(
            request.POST
        )
        context: dict = {
            'form': form,
        }
        return render(
            request,
            'login.html',
            context
        )


class RegisterView(View):
    
    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs:  dict
    ):

        form: CustomUserChangeForm = CustomUserChangeForm(
        request.POST
        )
        if form.is_valid():
            user: CustomUser = form.save(
                commit=False
            )
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user.email = email
            user.set_password(password)
            user.save()

            user: CustomUser = dj_authenticate(
                email=email,
                password=password
            )
            if user and user.is_active:

                dj_login(request, user)

                homeworks: QuerySet = Homework.objects.filter(
                    user=request.user
                )
                return render(
                    request,
                    'index.html',
                    {'homeworks': homeworks}
                )
        context: dict = {
            'form': form
        }
        return render(
            request,
            'register.html',
            context
        )


class HomeworkCreateView(ViewHandler, View):
    """Homework Create View."""

    form: HomeworkForm = HomeworkForm
    template_name: str = 'homework_create.html'

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """GET request handler."""

        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        context: dict = {
            'ctx_form': self.form(),
        }
        return self.get_http_response(
            request,
            self.template_name,
            context
        )

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:
        """POST request handler."""

        _form: HomeworkForm = self.form(
            request.POST or None,
            request.FILES or None
        )
        if not _form.is_valid():
            context: dict = {
                'ctx_form': _form,
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        homework: Homework = _form.save(
            commit=False
        )
        homework.user = request.user
        homework.logo = request.FILES['logo']

        file_type: str = homework.logo.url.split('.')[-1].lower()

        if file_type not in Homework.IMAGE_TYPES:

            context: dict = {
                'ctx_form': _form,
                'ctx_homework': homework,
                'error_message': 'PNG, JPG, JPEG',
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        homework.save()

        context: dict = {
            'homework': homework
        }
        return self.get_http_response(
            request,
            'university/homework_detail.html',
            context
        )