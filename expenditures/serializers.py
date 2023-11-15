from django.contrib.auth import get_user_model


from rest_framework import serializers

from budgets.models import Category, Budget
from expenditures.models import Expenditure
from accounts.serializers import UserSerializer

User = get_user_model()


class ExpenditureListSerializer(serializers.ModelSerializer):
    class Meta():
        model = Expenditure
        fields = '__all__'


class ExpenditureCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = Expenditure
        fields = ['user', 'category', 'amount', 'memo', 'appropriate_amount']
    
    def create(self, validated_data):
        return Expenditure.objects.create(**validated_data)