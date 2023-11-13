from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from accounts.serializers import UserTotalUpdateSerializer
from budgets.models import Budget, Category, REC_LIST, BUDGET_REC_RATIO
from budgets.serializers import CategorySerializer, BudgetCreateSerializer


class CategoryListView(ListAPIView):
    '''
    method: GET
    소비 카테고리 리스트 반환
    '''
    permission_classes = [AllowAny,]
    # permission_classes = [IsAuthenticated,]
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')


class BudgetsView(APIView):
    '''
    method: GET, POST, PATCH
    '''
    
    # permission_classes = [AllowAny, ]
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        '''
        소비 카테고리 리스트 반환
        '''
        queryset = Category.objects.all().order_by('id')
        serializer = CategorySerializer(queryset, many=True)
        
        return Response({
            "message": "get categories",
            "data": serializer.data},
            status=status.HTTP_200_OK
            )
    
    def post(self, request):
        '''
        예산 종목별 금액입력
        '''
        data = request.data
        budget_list = data.get('budget_list', None)
        result = []
        total = 0
        user = request.user
        
        ## TODO-같은 카테고리 들어왔을 때 처리 추가 필요.
        # 동혁님. unique_together? unique_constrain?
        # djagno 복합key 설정 못함. 단일 key설정임
        # 이 복합 key 대신 두 필드에 unique를 걸어주는 것.
        if budget_list:
            for budget in budget_list:
                total += budget.get("amount", 0)
                budget["user"] = user.pk
                serializer = BudgetCreateSerializer(data=budget)
                if serializer.is_valid():
                    result.append(serializer.create(serializer.validated_data).pk)
        
        total_serializer = UserTotalUpdateSerializer(data={'total': total})
        if total_serializer.is_valid():
            user = total_serializer.update(user, total_serializer.validated_data)

        return Response({
            "message": "budget create success!",
            "setup_user": user.pk,
            "setup_user_total": user.total,
            "data": result
            },
            status=status.HTTP_201_CREATED
            )

    def patch(self, request, ):
        '''
        예산 수정
        '''
        ## 여러개 레코드가 생기는데.. 어떻게 수정을 해야할지 고민중..
        ## 원래거 전체 삭제하고 전체 싹다 받아서 해야하나요
        pass

