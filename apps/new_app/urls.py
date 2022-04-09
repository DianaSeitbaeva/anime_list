from django.urls import (
    path,
    re_path,
)
from django.conf import settings
from django.conf.urls.static import static

from new_app import views
from new_app.views import (
    IndexView,
    RegisterView,
    LoginView,
    LogoutView,
    HomeworkCreateView,
)

urlpatterns = [

    path(
        '', 
        IndexView.as_view(),
        name='page_main'
    ),
    path(
        'show/<int:homework_id>/',
        views.show,
        name='page_show'
    ),
    path(
        'register/', 
        RegisterView.as_view(), 
        name='page_register'),
    path(
        'login/',
        LogoutView.as_view(),
        name='page_login'),
    path(
        'logout/', 
        LogoutView.as_view(), 
        name='page_logout'),
] + static(
    settings.STATIC_URL, 
    document_root=settings.STATIC_ROOT
)