from django.contrib.auth import get_user_model


from rest_framework import serializers

from budgets.models import Category, Budget
from expenditures.models import Expenditure
from accounts.serializers import UserSerializer

User = get_user_model()


class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta():
        model = Expenditure
        fields = '__all__'
        
    def update(self, instance, validated_data):
        # instance.user = validated_data.get("user", instance.user)
        instance.category = validated_data.get("category", instance.category)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.memo = validated_data.get("memo", instance.memo)
        instance.appropriate_amount = validated_data.get("appropriate_amount", instance.appropriate_amount)
        instance.is_exept = validated_data.get("is_exept", instance.is_exept)
        
        result = instance.save()
        return instance, result


class ExpenditureCreateSerializer(serializers.ModelSerializer):
    class Meta():
        model = Expenditure
        fields = ['user', 'category', 'amount', 'memo', 'appropriate_amount', 'is_exept']
    
    def create(self, validated_data):
        return Expenditure.objects.create(**validated_data)
    

class ExpenditureUpdateSerializer(serializers.ModelSerializer):
    class Meta():
        model = Expenditure
        fields = ['category', 'amount', 'memo']