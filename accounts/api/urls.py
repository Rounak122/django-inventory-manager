from accounts.api.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'
urlpatterns = [
    path('create_user', create_user),
    path('login_user', obtain_auth_token),
    path('get_user', get_user),
    path('update_user', update_user),
    # path('logout_user', Logout.as_view()),
]
