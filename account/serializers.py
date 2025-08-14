from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "role", "mobile")

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role", "mobile")
        read_only_fields = ("id", "email", "role")

    # def validate(self, attrs):
    #     # If role is being updated, raise error
    #     if 'email' in attrs:
    #         raise serializers.ValidationError({
    #             'email': "You are not allowed to update the email."
    #         })
    #     if 'role' in attrs:
    #         raise serializers.ValidationError({
    #             'role': "You are not allowed to update the role."
    #         })
    #     return attrs
    
    def update(self, instance, validated_data):
        allowed_fields = ['first_name', 'last_name', 'mobile']
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data['user'] = user
        return data
    
