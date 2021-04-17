from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
# from rest_framework.filters import SearchFilter, OrderingFilter

from accounts.models import Account
from products.models import Product
from products.api.serializer import ProductSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request):

    try:
        if request.method == 'GET':
            if 'key' in request.GET.keys():
                key = request.GET.get('key')
                try:
                    product = Product.objects.get(pk=key)
                    user = request.user
                    if user != product.owner:
                        return Response({"message": "permission not granted"}, status=status.HTTP_403_FORBIDDEN)

                except Product.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = ProductSerializer(product)
                return Response(serializer.data)
            else:
                user = request.user
                product = Product.objects.filter(owner=user)
                serializer = ProductSerializer(product, many=True)
                return Response(serializer.data)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_product(request):

    try:
        if request.method == 'PATCH':
            key = request.GET.get('key')
            try:
                product = Product.objects.get(pk=key)
                user = request.user
                if user != product.owner:
                    return Response({"message": "permission not granted"}, status=status.HTTP_403_FORBIDDEN)

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
@permission_classes([IsAuthenticated])
def create_product(request):

    owner = request.user
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
@permission_classes([IsAuthenticated])
def delete_product(request):

    try:
        if request.method == 'DELETE':
            key = request.GET.get('key')
            try:
                product = Product.objects.get(pk=key)
                user = request.user
                if user != product.owner:
                    return Response({"message": "permission not granted"}, status=status.HTTP_403_FORBIDDEN)

            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            is_deleted = product.delete()

            if is_deleted:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListProducts(ListAPIView):

    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['name', 'code']

    def get(self, request):
        user = request.user
        queryset = Product.objects.filter(owner=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
