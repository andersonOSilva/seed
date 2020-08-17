from django.shortcuts import render
from django.http import Http404

from .serializer import UserSerializer
from .serializer import UserListSerializer
from .serializer import NaverSerializer
from .serializer import NaverListSerializer

from .models import User
from .models import Naver

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class UserListView(APIView):
    """
    View que lista e cadastra usuário.
    """
    serializer_class = UserSerializer
    serializer_detail_class = UserListSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        serializer = self.serializer_detail_class(User.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    """
    View que mostra, altera e apaga usuário.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_User(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, email, format=None):
        User = self.get_User(email)
        serializer = self.serializer_class(User)
        return Response(serializer.data)

    def patch(self, request, email, format=None):
        User = self.get_User(email)
        serializer = self.serializer_class(User, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email, format=None):
        User = self.get_User(email)
        User.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class Login(APIView):
    """
    View efetua login retornando token JWT.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        if email is None:
            return Response({
                                'error': 'Email not informed'
                            }, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(email=email)
            if not user.check_password(request.data['password']):
                return Response({
                                    'error': 'Wrong email or password'
                                }, status=status.HTTP_400_BAD_REQUEST)

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({
                        "token": token,
                        "user": UserListSerializer(
                            user, context={
                                'request': request
                                            }).data}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({
                                'error': 'User not found'
                            }, status=status.HTTP_403_FORBIDDEN)
