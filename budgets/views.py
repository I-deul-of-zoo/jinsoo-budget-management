from django.shortcuts import render
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from accounts.serializers import UserParamUpdateSerializer
from budgets.models import Budget, Category, REC_LIST, BUDGET_REC_RATIO
from budgets.serializers import CategorySerializer, BudgetSerializer



def update_user_parameter(total, start):
    total_serializer = UserParamUpdateSerializer(data={"total": total, "start_date": start})
    if total_serializer.is_valid():
        user = total_serializer.update(user, total_serializer.validated_data)
    return None

class BudgetsView(APIView):
    '''
    method: GET, POST, PATCH
    '''
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
    
    def post(self, request, pk):
        '''
        예산 종목별 금액입력
        '''
        data = request.data
        budget_list = data.get('budget_list', None)
        start_date = data.get("start_date", None)
        result = []
        total = 0
        user = request.user
        
        ## TODO - 중복입력처리 view에서 >>  serializer에서 하는 방법 알아보기
        try:
            check_list = [budget.get("category") for budget in budget_list]
            for ch in check_list:
                if check_list.count(ch) > 1:
                    raise ValidationError(f"override category: {ch}")
        except ValidationError as ve:
            return Response({"message": "input error", "error": ve.message})
        
        ## 뷰에서 하나씩 처리
        if budget_list:
            for budget in budget_list:
                total += budget.get("amount", 0)
                budget["user"] = user.pk
                serializer = BudgetSerializer(data=budget)
                if serializer.is_valid():
                    result.append(serializer.create(serializer.validated_data))
        
        # for b in budget_list:
        #     b["user"] = user.pk
            
        # serializer = BudgetSerializer(data=budget_list, many=True)
        # try:
        #     if serializer.is_valid():
        #         serializer.create()
        # except:
        #     return Response({"message": "error", "error": serializer.errors})
        
        update_user_parameter(total=total, satrt=start_date)

        return Response({
            "message": "budget create success!",
            "setup_user": user.pk,
            "setup_user_total": user.total,
            "data": result
            },
            status=status.HTTP_201_CREATED
            )

    def patch(self, request):
        '''
        예산 수정
        '''
        ## 1개의 레코드만 선택적으로 수정한다고 가정.
        ## TODO - 카테고리가 없는 부분에 대해서 처리가 부족.
        data = request.data
        user = request.user
        start_date = data.get("start_date", None)
        queryset = Budget.objects.filter(user=user.pk)
        budget_list = list(queryset)
        
        if data.get("category", None) is None:
            # raise ValueError("message: no content!") ## 기능이 동작하는 도중에 알려주는 용도?
            return Response({"message": "no content!"}, status=status.HTTP_204_NO_CONTENT) ## 여기서 끝나야 할 때
        
        if not budget_list:
            return Response({"message": f"failed! {user.username} has no budgets"}, status=status.HTTP_404_NOT_FOUND)
        
        budget = queryset.get(category=data.get("category"))
        change_amount = data.get("amount") - budget.amount
        serializer = BudgetSerializer(instance=budget, data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.update(budget, serializer.validated_data)
            
            # user의 total 변화에 반영
            new_total = user.total - change_amount
            update_user_parameter(total=new_total, satrt=start_date)
            
            return Response({"message": "success!", "data": f"Budget[{instance.pk}] - category{instance.category.name} is changed.({instance.amount})"}, status=status.HTTP_200_OK)


class BudgetRecommendView(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        '''
        스타일로 입력할 수 있는 값의 목록을 전달합니다.
        '''
        return Response({
            "message": "recommend styles",
            "data": REC_LIST},
            status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        선택한 스타일로 예산을 설정합니다.
        '''
        total = request.data.get("total")
        style = request.data.get("style", REC_LIST[0])
        start_date = request.data.get("start_date", None)
        user = request.user
        result = []
        update_user_parameter(total=total, satrt=start_date)
            
        if style in REC_LIST:
            for budget in BUDGET_REC_RATIO.get(style):
                budget["user"] = user.pk
                ratio = budget.get("ratio")
                budget["amount"] = int(round(user.total * ratio / 100, -1)) # 10의자리에서 반올림
                serializer = BudgetSerializer(data=budget)

                if serializer.is_valid():
                    result.append(serializer.create(serializer.validated_data).pk)
            
            return Response(
                {
                    "message": "suceess!",
                    "setup_user": user.pk,
                    "setup_user_total": user.total,
                    "data": result
                },
                status=status.HTTP_201_CREATED
                )
            
        return Response({"message": "failed."}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request):
        '''
        예산 수정
        스타일 지정 변경이기 때문에 해당되지 않는 카테고리는 0으로 만들어버림
        없었던 budget 카테고리 행은 생성
        '''
        # TODO - View 코드가 너무 길어지는데... 간단하게 하는 방법 없을까...?
        
        user = request.user
        data = request.data
        start_date = data.get("start_date", None)
        new_total = data.get("total", None)
        new_style = data.get("style", None)
        queryset = Budget.objects.filter(user=user.pk)
        budget_list = list(queryset)
        
        if budget_list is None:
            return Response({"message": f"failed! {user.username} has no budgets"}, status=status.HTTP_404_NOT_FOUND)
        
        if new_total is not None:
            update_user_parameter(total=new_total, satrt=start_date)
        
        if new_style in REC_LIST:
            update_list = BUDGET_REC_RATIO[new_style]
            check_list = [b.get("category") for b in update_list]
            
            # 있는데 없어지거나 변경되는 경우
            for new_data in update_list:
                for budget in budget_list:
                    if budget.category.pk == new_data.get("category"):
                        ratio = new_data.get("ratio")
                        new_data["amount"] = int(round(user.total * ratio / 100, -1))
                        serializer = BudgetSerializer(data=new_data, partial=True)
                        if serializer.is_valid():
                            serializer.update(budget, serializer.validated_data)
                        new_data["checked"] = True
                    elif budget.category.pk in check_list:
                        continue
                    else:
                        serializer = BudgetSerializer(data={"category": budget.category.pk, "ratio":0, "amount":0}, partial=True)
                        if serializer.is_valid():
                            serializer.update(budget, serializer.validated_data)
            
            ## 없다가 새로 생기는 경우
            for d in update_list:
                if d.get("checked", None) is None:
                    d["user"] = user.pk
                    ratio = d.get("ratio")
                    d["amount"] = int(round(user.total * ratio / 100, -1))
                    serializer = BudgetSerializer(data=d)
                    if serializer.is_valid():
                        serializer.create(serializer.validated_data)
                    
            return Response({"message": "style change success", "data": new_style}, status=status.HTTP_200_OK)
                    
        return Response({"message": "no exist style", "error": new_style}, status=status.HTTP_400_BAD_REQUEST)
    