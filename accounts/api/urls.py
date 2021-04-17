from accounts.api.views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'
urlpatterns = [
    path('create_user', create_user),
    path('login_user', ObtainAuthTokenView.as_view()),
    path('get_user', get_user),
    path('update_user', update_user),
    path('check_user_exists', does_account_exist_view,
         name="check_if_account_exists"),
    path('change_user_password', ChangePasswordView.as_view(),
         name="change_password"),
    path('email-verify', VerifyEmail.as_view(), name='email-verify'),
    # path('logout_user', Logout.as_view()),
]
