from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from budgets.models import Category, Budget

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta():
        model=Category
        fields = '__all__'