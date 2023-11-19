from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from .models import Product
from .serializers import ProductSerializer
from .usecases import AuthApiView

class ProductViewSet(AuthApiView, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Установка текущего пользователя в качестве владельца продукта при создании
            serializer.save(user=self.request.user)
        else:
            # Если пользователь не аутентифицирован, можете предпринять соответствующие действия
            # например, выбросить ошибку, установить другого пользователя или установить значение по умолчанию.
            pass

    @api_view(['GET', 'POST'])
    def product_list(request):
        if request.method == 'GET':
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET', 'PUT', 'DELETE'])
    def product_detail(request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
      