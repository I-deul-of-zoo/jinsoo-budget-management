import math
import copy
from pytz import timezone
from datetime import date, datetime, timedelta
import calendar

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

def unpack_cat_stat(cat_static:dict)->(str,dict):
    name = list(cat_static.keys())[0]
    value = list(cat_static.values())[0]
    return name, value

def get_expend_statistics(expenditure_set)-> dict:
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
    

def get_base_datetime(today: datetime, user_start_date:int)->datetime:
    return datetime(year=today.year, month=today.month, day=user_start_date)


def get_aspected_expenditure(user, today, period=30)->(dict,dict):
    '''
    어제까지의 소비 내용을 기반으로 오늘 소비 추천내용
    '''
    result = dict()
    
    base_dt = get_base_datetime(today, user.start_date)
    today_dt = datetime.strptime(str(today), "%Y-%m-%d")
    current = today_dt - base_dt # current.days==현재일-1
    
    budget_set = Budget.objects.filter(user=user.pk)
    expend_set = Expenditure.objects.filter(
        user=user.pk, 
        created_at__gte=base_dt, 
        created_at__lt=today_dt)
    
    ## 리스트 통계 데이터 생성
    static_result = get_expend_statistics(expend_set)
    
    ## 총 예산에 대한 현재 결과
    remain = user.total - static_result["total_sum"]
    recommend_budget = math.floor((remain/(period - current.days - 1))/100)*100
    result["today_recommand"] = recommend_budget
    result["period"] = f"{base_dt} ~ {today_dt}"
    
    ## 각 카테고리 예산에 대한 결과
    calib_minimum = 0
    cat_exp_list = static_result["category_group"] # list
    for b in budget_set:
        cat_sum = 0
        for cat_exp in cat_exp_list:
            if b.category.name in cat_exp.keys():
                cat_sum = cat_exp[b.category.name]["sum"]
                
        cat_remain = b.amount - cat_sum
        if cat_remain < 0:
            calib_minimum += (3330 + (-1 * cat_remain))
            cat_recommend_budget = 3330
        else:
            cat_recommend_budget = math.floor((cat_remain/(period - current.days))/100)*100
        result[b.category.name] = cat_recommend_budget
    
    result["today_recommand"] += calib_minimum
    
    return result, static_result


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
        static_result = get_expend_statistics(queryset)
        
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
        today = date.today()
        period = calendar.monthrange(today.year, today.month)[1]
        base_dt = get_base_datetime(today, user.start_date)
        today_dt = datetime.strptime(str(today), "%Y-%m-%d")
        current = today_dt - base_dt # current.days==현재일-1
        
        result, static_result = get_aspected_expenditure(user=user, today=today, period=period)
        
        ## 소비 현황에 대한 메시지
        budget_per_date = user.total/period
        aspect_expend = budget_per_date * current.days
        
        message = f"today({str(today)})'s message: "
        if (aspect_expend * UNDER) < static_result["total_sum"]:
            message += "very good~~! :)"
        elif (aspect_expend * UNDER) <= static_result["total_sum"] and (aspect_expend * UPPER) <= static_result["total_sum"]:
            message += "not bad~~ ~.~"
        else:
            message += "you have to save your money!"
            
        return Response({"message": message, "data": result}, status=status.HTTP_200_OK)
    


class ExpenditureNotificationToday(APIView):
    def get(self, request):
        user = request.user
        result = dict()
        
        ## TODO - 예산목록과 지출목록을 호출하는 부분을 모듈화해서 호출하는게 좋아보입니다.
        today = date.today()
        period = calendar.monthrange(today.year, today.month)[1]
        base_dt = get_base_datetime(today, user.start_date)
        today_start_dt = datetime.strptime(str(today), "%Y-%m-%d")
        today_end_dt = today_start_dt + timedelta(days=1)
        current = today_start_dt - base_dt
        remain_days = period - current.days
        
        expend_today_set = Expenditure.objects.filter(
            user=user.pk, 
            created_at__gte=today_start_dt, 
            created_at__lt=today_end_dt)
        
        today_static_result =get_expend_statistics(expend_today_set)
        
        
        # 오늘 이전 소비를 통해 오늘 권장 소비 내용.
        result, static_result = get_aspected_expenditure(user=user, today=today, period=period)
        
        rate_result = dict()
        total_rate = math.floor(100*today_static_result["total_sum"]/result["today_recommand"])
        
        rate_result["total"] = total_rate
        for cat in today_static_result["category_group"]:
            name, value = unpack_cat_stat(cat)
            rate = -1
            if result.get(name, None):
                rate = math.floor(100*value["sum"]/result[name])
            rate_result[name] = rate
        
        rate_result["unit"] = "percent"
        
        return Response({"message": "success!", "data": rate_result, "recommend_data":result}, status=status.HTTP_200_OK)