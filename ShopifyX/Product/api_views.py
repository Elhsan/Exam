from django.forms import model_to_dict
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .usecases import *
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ModelViewSet):
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