from django.contrib.auth import get_user_model


from rest_framework import serializers

from budgets.models import Category, Budget
from accounts.serializers import UserSerializer

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Category
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Budget
        # fields = '__all__'
        fields = ['user', 'category', 'amount', 'ratio']
    
    def create(self, validated_data):
        return Budget.objects.create(**validated_data)
    
    # def validate(self, data):
    #     # print(self.initial_data) ## many=True로 했을 때 리스트로 들어옴
    #     # print(data) ## 한개
        
    #     # 객체 개수만큼 실행된다는 단점이 있음. 해결할 방법이 있을까?
    #     # View에 직접 코딩하는것 이외에..
    #     if isinstance(self.initial_data, list):
    #         check_list = [init.get("category") for init in self.initial_data]
    #         print(check_list)
    #         for ch in check_list:
    #             if check_list.count(ch) > 1:
    #                 raise ValidationError(f"override category: {ch}")

    #         print("리스트로 들어왔어요~")
        
    #     if isinstance(self.initial_data, dict):
    #         print("한개로 들어왔어요~~")
        
    #     return data
    
    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount", instance.amount)
        instance.ratio = validated_data.get("ratio", instance.ratio)
        instance.save()

        return instance
    

