import math
import copy
from datetime import date, datetime, timedelta

from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from expenditures.models import Expenditure
from expenditures.serializers import ExpenditureSerializer, ExpenditureCreateSerializer, ExpenditureUpdateSerializer

from budgets.models import CATEGORIES

STATIC_FORM = dict.fromkeys(CATEGORIES.keys(), {"count":0, "sum":0})
DICT_FORM = {"count":0, "sum":0}


class ExpenditureListCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        '''
        리스트 보기
        '''
        user = request.user
        queryset = Expenditure.objects.filter(user=user.pk)
        
        query_params = request.query_params
        start = query_params.get("start", str(date.today() - timedelta(days=30)))
        end = query_params.get("end", str(date.today()))
        category = query_params.get("category", "all")
        min_amount = query_params.get("min", 0)
        max_amount = query_params.get("max", 9999999999) ## 예산 최대값을 어떻게 정할 수 있을까?
        
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date =  datetime.strptime(end, '%Y-%m-%d')
        end_date = end_date + timedelta(days=1)
        
        queryset = queryset.filter(created_at__gte=start_date, created_at__lt=end_date, amount__gte=min_amount, amount__lt=max_amount)
        
        if category != "all":
            queryset = queryset.filter(category=category)
        
        serializer = ExpenditureSerializer(queryset, many=True)
        result = serializer.data
        
        ## 리스트 통계 데이터 생성
        statistics = dict()
        temp_list = list()
        for keyname in CATEGORIES.keys():
            temp_list.append({keyname: copy.deepcopy(DICT_FORM)})
            
        statistics["category_group"] = temp_list
        total = 0
        for q in list(queryset):
            total += q.amount
            for d in statistics["category_group"]:
                if d.get(q.category.name, None):
                    d[q.category.name]["count"] += 1
                    d[q.category.name]["sum"] += q.amount
        
        statistics["total_sum"] = total

        return Response({"message": "success!", "data": result, "static_data":statistics}, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        생성
        
        {
            "category" : 4,
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