from django.urls import path
from auths.views import ListUsers


app_name = 'auths'

urlpatterns = [
    path('users', ListUsers.as_view(), name='users')
]