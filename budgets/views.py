
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render

from budgets.models import Budget, Category
from budgets.serializers import CategorySerializer


class CategoryListView(ListAPIView):
    '''
    '''
    permission_classes = [AllowAny,]
    # permission_classes = [IsAuthenticated,]
    
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')
    