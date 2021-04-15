from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.generics import ListAPIView
# from rest_framework.filters import SearchFilter, OrderingFilter

from accounts.models import Account
from products.models import Product
from products.api.serializer import ProductSerializer
# from blog.models import BlogPost
# from blog.api.serializers import BlogPostSerializer, BlogPostUpdateSerializer, BlogPostCreateSerializer


@api_view(['GET'])
def get_product(request):

    try:
        if request.method == 'GET':
            if 'key' in request.GET.keys():
                key = request.GET.get('key')
                try:
                    product = Product.objects.get(pk=key)

                except Product.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = ProductSerializer(product)
                return Response(serializer.data)
            else:
                product = Product.objects.all()
                serializer = ProductSerializer(product, many=True)
                return Response(serializer.data)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_product(request):

    try:
        if request.method == 'PATCH':
            key = request.GET.get('key')
            try:
                product = Product.objects.get(pk=key)

            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = ProductSerializer(product, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_product(request):

    owner = Account.objects.get(pk=1)
    new_product = Product(owner=owner)

    try:
        if request.method == 'POST':

            serializer = ProductSerializer(new_product, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_product(request):

    try:
        if request.method == 'DELETE':
            key = request.GET.get('key')
            try:
                product = Product.objects.get(pk=key)

            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            is_deleted = product.delete()

            if is_deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
