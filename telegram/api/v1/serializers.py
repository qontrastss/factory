from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from telegram.models import Message


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name')
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True},
                        'username': {'required': True},
                        'first_name': {'required': True}}

    def validate_password(self, value):
        # Validate the password using Django's built-in password validators
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name']
        )
        return user


class MessageBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'created_at')
