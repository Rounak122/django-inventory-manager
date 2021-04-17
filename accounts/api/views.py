from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import GenericAPIView  # CAN BE DELETED
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from accounts.models import Account
from accounts.api.serializer import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from accounts.utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_user(request):
    data = {}

    try:
        if request.method == 'POST':
            email = request.data.get('email', '0').lower()
            if validate_email(email) != None:
                data['error_message'] = 'This email is already in use.'
                data['error'] = True
                return Response(data)

            username = request.data.get('username', '0')
            if validate_username(username) != None:
                data['error_message'] = 'That username is already in use.'
                data['error'] = True
                return Response(data)

            mobile = request.data.get('mobile_number', '0')
            if validate_mobile(mobile) != None:
                data['error_message'] = 'That mobile number is already in use.'
                data['error'] = True
                return Response(data)

            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                account = serializer.save()
                token = Token.objects.get(user=account).key

                current_site = get_current_site(request).domain
                # relativeLink = reverse('email-verify')
                relativeLink = 'email-verify'

                absurl = 'http://'+current_site + "/api/accounts/" + \
                    relativeLink+"?token="+str(token)
                email_body = 'Hello '+request.data.get('first_name') + ",\n" + 'Click the following link to verify your account \n' + \
                    absurl + "\n" + "Regards, \nRounak, \nFounder -  QR Inventory Manager"
                data = {'email_body': email_body, 'to_email': email,
                        'email_subject': 'Verify your Account | QR Inventory Manager'}

                Util.send_email(data)

                data['response'] = 'successfully registered new user.'
                data["user"] = serializer.data
                data["token"] = token
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data['error'] = True
                data['response'] = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def validate_email(email):
    account = None
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_mobile(mobile):
    account = None
    try:
        account = Account.objects.get(mobile_number=mobile)
    except Account.DoesNotExist:
        return None
    if account != None:
        return mobile


def validate_username(username):
    account = None
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


class VerifyEmail(APIView):

    authentication_classes = []
    permission_classes = []

    # serializer_class = EmailVerificationSerializer

    # token_param_config = openapi.Parameter(
    #     'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            # payload = jwt.decode(token, settings.SECRET_KEY)
            print(token)
            user_id = Token.objects.get(key=token).user_id
            print(user_id)
            user = Account.objects.get(id=user_id)
            if not user.is_active:
                user.is_active = True
                user.save()
            return HttpResponse('<h1>Account Successfully activated, Login to the app</h1>')
        except:
            return HttpResponse('<h1>Invalid token, please try again</h1>')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    data = {}

    try:
        account = request.user
    except Account.DoesNotExist:
        data['error'] = True
        data['response'] = "User Not Found"
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    serializer = UserDetailsSerializer(account)

    data['error'] = False
    data['response'] = serializer.data
    return Response(data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):

    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserDetailsSerializer(
        account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        data = {}
        data["message"] = "user updated"
        data["user"] = serializer.data
        return Response(data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class Logout(APIView):
#     def post(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)


# Login
class ObtainAuthTokenView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.POST.get('username')
        password = request.POST.get('password')
        # print(request.POST)
        # print(password)
        account = authenticate(email=email, password=password)
        # print(account)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['token'] = token.key
            context['error'] = False
        else:
            context['error'] = True
            context['message'] = 'Invalid credentials'

        return Response(context)


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):

    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            account = Account.objects.get(email=email)
            data['error'] = False
            data['response'] = email
        except Account.DoesNotExist:
            data['error'] = True
            data['response'] = "Account does not exist"
        return Response(data)


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
