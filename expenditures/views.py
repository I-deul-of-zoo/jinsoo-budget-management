from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


class ExpenditureView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        pass
    
    def post(self, request):
        pass
    def patch(self, request):
        pass
    
    def delete(self, request):
        pass