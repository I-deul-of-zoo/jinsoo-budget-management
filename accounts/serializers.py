from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = '__all__'
        
    def create(self, **validated_data):
        user = User(
            username=validated_data.get('username')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
        
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('An username address is required to log in.')
        
        if password is None:
            raise serializers.ValidationError('A password is required to log in.')
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found')
        
        return {'username': user.username, 'user': user}
    

class UserTotalUpdateSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    
    def update(self, instance, validated_data):
        instance.total = validated_data.get('total', instance.total)
        instance.save()
        return instance