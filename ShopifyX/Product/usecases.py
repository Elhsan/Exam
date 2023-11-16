from .models import Product
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductSerializer

class Session:
    def __init__(self, request):
        self.session = request.session

    def get(self, key, default=None):
        self._check_key(key)
        return self.session.get(key, default)

    def set(self, key, value):
        self._check_key(key)
        self.session[key] = value

    def update(self, key, value):
        self._check_key(key)
        self.session[key].update(value)


class NoAuthApiView(APIView):
    """Doesn't require authentication"""
    permission_classes = [AllowAny]

class AuthApiView(NoAuthApiView):
    """Requires authentication"""
    permission_classes = [IsAuthenticated]