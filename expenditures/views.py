from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from expenditures.models import Expenditure
from expenditures.serializers import ExpenditureListSerializer, ExpenditureCreateSerializer

class ExpenditureListCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        '''
        리스트 보기
        '''
        user = request.user
        queryset = Expenditure.objects.filter(user=user.pk)
        serializer = ExpenditureListSerializer(queryset, many=True)
        result = serializer.data

        return Response({"message": "sucess!", "data": result}, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        생성
        
        {
            "category" : 4,
            "
        }
        '''
        user = request.user
        data = request.data
        data["user"] = user.pk
        data["appropriate_amount"] = 10000 ## 아직 10000
        print(data)
        
        serializer = ExpenditureCreateSerializer(data=data)
        
        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            
            if result:
                return Response({"message": "success!", "data": data}, status=status.HTTP_200_OK)
        
        return Response({"message": "crate fail!"}, status=status.HTTP_400_BAD_REQUEST)


class ExpenditureView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, ex_pk):
        '''
        상세보기
        '''
        pass
    
    def patch(self, request, ex_pk):
        '''
        수정
        '''
        pass
    
    def delete(self, request, ex_pk):
        '''
        삭제
        '''
        pass