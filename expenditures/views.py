import math
import copy
from pytz import timezone
from datetime import date, datetime, timedelta

from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from config import settings
from budgets.models import Budget
from budgets.models import CATEGORIES
from expenditures.models import Expenditure
from expenditures.serializers import ExpenditureSerializer, ExpenditureCreateSerializer, ExpenditureUpdateSerializer


## constanct
CAT_STAT_FORM = {"count":0, "sum":0}
UNDER = 0.95
UPPER = 1.05

def statistic_info(expenditure_set)-> dict:
        result = dict()
        temp_list = list()
        for keyname in CATEGORIES.keys():
            temp_list.append({keyname: copy.deepcopy(CAT_STAT_FORM)})
            
        result["category_group"] = temp_list
        total = 0
        for q in list(expenditure_set):
            total += q.amount
            for d in result["category_group"]:
                if d.get(q.category.name, None):
                    d[q.category.name]["count"] += 1
                    d[q.category.name]["sum"] += q.amount
        
        result["total_sum"] = total
        return result
    

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
        data_result = serializer.data
        
        ## 리스트 통계 데이터 생성
        static_result = statistic_info(queryset)
        
        return Response({"message": "success!", "data": data_result, "static_data":static_result}, status=status.HTTP_200_OK)
    
    
    
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
    

class ExpenditureRecommendToday(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        # 기준 시작일을 어떻게 가져갈 것인지?
        # 1. 매월 1일을 기준으로..
        # 2. 매월 n일을 기준으로 설정. >> 첫 예산 생성 날짜 적용
        # >> 유저에게 등록한 start_date를 기준으로 산정합니다.
        user = request.user
        result = dict()
        
        ## TODO - 예산목록과 지출목록을 호출하는 부분을 모듈화해서 호출하는게 좋아보입니다.
        end = date.today()
        start = date(year=end.year, month=end.month, day=user.start_date)
        end_date = datetime.strptime(str(end), "%Y-%m-%d")
        start_date = datetime.strptime(str(start), '%Y-%m-%d')
        # end_date.astimezone(timezone(settings.TIME_ZONE))
        # start_date.astimezone(timezone(settings.TIME_ZONE))
        current = end_date - start_date # 15 days. 15보려면 current.days
        
        budget_set = Budget.objects.filter(user=user.pk)
        expend_set = Expenditure.objects.filter(user=user.pk, created_at__gte=start_date, created_at__lt=end_date)
        
        ## 리스트 통계 데이터 생성
        static_result = statistic_info(expend_set)
        
        ## 총 예산에 대한 현재 결과
        budget_per_date = user.total/30
        aspect_expend_today = budget_per_date * current.days
        remain = user.total - aspect_expend_today
        recommend_budget = math.floor((remain/(30 - current.days - 1))/100)*100
        result["today_total"] = recommend_budget
        
        ## 각 카테고리 예산에 대한 결과
        for b in budget_set:
            cat_per_date = b.amount/30
            aspect_cat_today = cat_per_date * current.days
            cat_remain = b.amount - aspect_cat_today
            cat_recommend_budget = math.floor((cat_remain/(30 - current.days - 1))/100)*100
            result[b.category.name] = cat_recommend_budget
        
        ## 메시지 수정
        message = f"today({str(end)})s message: "
        if (aspect_expend_today * UNDER) < static_result["total_sum"]:
            message += "very good~~! :)"
        elif (aspect_expend_today * UNDER) <= static_result["total_sum"] and (aspect_expend_today * UPPER) <= static_result["total_sum"]:
            message += "not bad~~ ~.~"
        else:
            message += "you have to save your money!"
            
        return Response({"message": message, "data": result}, status=status.HTTP_200_OK)