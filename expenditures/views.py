from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from expenditures.models import Expenditure
from expenditures.serializers import ExpenditureSerializer, ExpenditureCreateSerializer, ExpenditureUpdateSerializer

class ExpenditureListCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        '''
        리스트 보기
        '''
        user = request.user
        queryset = Expenditure.objects.filter(user=user.pk)
        serializer = ExpenditureSerializer(queryset, many=True)
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
        ## TODO - 입력 검증 부분 필요
        
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
        expend = get_object_or_404(Expenditure, pk=ex_pk)
        serializer = ExpenditureSerializer(expend)
        
        return Response({"message": "get sucess!", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, ex_pk):
        '''
        전체수정
        '''
        ## TODO - 필요한가?
        pass
    
    def patch(self, request, ex_pk):
        '''
        부분수정
        '''
        ## TODO - 입력 검증 부분 필요
        instance = get_object_or_404(Expenditure, pk=ex_pk)
        data = dict(request.data)
        serializer = ExpenditureSerializer(data=data, partial=True)
        
        if serializer.is_valid():
            instance = serializer.update(instance, serializer.validated_data)
            print(instance)
            return Response({"message": "update sucess!"}, status=status.HTTP_200_OK)
        
        return Response({"message": "update failed!"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, ex_pk):
        '''
        삭제
        '''
        instance = get_object_or_404(Expenditure, pk=ex_pk)
        serializer = ExpenditureSerializer(instance)
        data = serializer.data
        instance.delete()
        
        return Response({"message": "delete sucess!", "data": data}, status=status.HTTP_200_OK)