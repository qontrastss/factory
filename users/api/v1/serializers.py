import datetime

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, validators

from users.models import User
import re


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'first_name')
#         extra_kwargs = {'password': {'write_only': True,
#                                      'required': True},
#                         'username': {'required': True},
#                         'first_name': {'required': True}}
#
#     def validate_password(self, value):
#         # Validate the password using Django's built-in password validators
#         try:
#             validate_password(value)
#         except ValidationError as e:
#             raise serializers.ValidationError(e.messages)
#
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name']
#         )
#         return user
#
#
# class UserRegistrationResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name')
#
#
# class UserAuthSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150)
#     password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    age = serializers.SerializerMethodField()

    def get_age(self, obj):
        return round((datetime.date.today() - obj.birth_date).days / 365) - 1

    class Meta:
        model = User
        fields = ['phone', 'password', 'created_at', 'first_name', 'birth_date', 'age', 'profile_pic']

    def validate_phone(self, value):
        import re
        match = re.search("^\+77\d{9}$", value)
        if not match:
            raise serializers.ValidationError("Некорректный номер телефона")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate_birth_date(self, value):
        if (datetime.date.today() - value) > datetime.timedelta(days=18*365):
            return value
        else:
            raise serializers.ValidationError("Лицам младше 18 лет запрещено использовать портал")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['phone', 'password', 'created_at', 'first_name', 'birth_date', 'profile_pic']

    def validate_phone(self, value):
        if value:
            raise serializers.ValidationError("Поле 'phone' не принимается")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate_birth_date(self, value):
        if (datetime.date.today() - value) > datetime.timedelta(days=18*365):
            return value
        else:
            raise serializers.ValidationError("Лицам младше 18 лет запрещено использовать портал")

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance