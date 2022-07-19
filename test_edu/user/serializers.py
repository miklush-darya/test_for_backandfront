from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password_submit = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = [
            "email",
            "password",
            "password_submit",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_submit"]:
            raise serializers.ValidationError("Passwords unmatched")
        return super().validate(attrs)

    def create(self, validated_data, **kwargs):
        validated_data.pop("password_submit")
        return User.objects.create_user(**validated_data)


class UserBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_active",
            "is_superuser",
        ]


