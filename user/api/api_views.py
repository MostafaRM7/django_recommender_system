from django.contrib.auth import authenticate, login, get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import UserLoginSerializer


class LoginViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response(UserLoginSerializer(user).data)
        return Response({'detail': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
