from rest_framework import serializers
from django.contrib.auth import get_user_model

from budgets.models import Category, Budget

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Category
        fields = '__all__'


class BudgetCreateSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Budget
        fields = '__all__'
    
    def create(self, validated_data):
        budget = Budget.objects.create(**validated_data)
        return budget
    