from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny, ]
    
    def post(self, response):
        serializer = RegisterSerializer(data=response.data)
        
        if serializer.is_valid():
            user = serializer.create(**serializer.validated_data)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "register success!",
                "userinfo": serializer.data,
                "token":{
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            
        else:
            return Response(
                {
                    "error": "failed to regist",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    permission_classes = [AllowAny, ]
    # serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        # TODO - 이거는 왜 에러나는지 get_serializer 함수 공부 필요.
        # serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(res, status=status.HTTP_200_OK)