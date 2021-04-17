from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from accounts.api.serializer import *
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def create_user(request):

    try:
        if request.method == 'POST':

            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                data = {}
                account = serializer.save()
                token = Token.objects.get(user=account).key
                data["user"] = serializer.data
                data["token"] = token
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):

    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserDetailsSerializer(account)
    return Response(serializer.data)


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
