from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "phone", "avatar", "role", "status", "email")
        read_only_fields = ("id", "role", "status")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "phone", "email", "role")

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", User.ROLE_USER)
        user = User.objects.create_user(role=role, **validated_data)
        return user


class PasswordLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError("用户名或密码错误")
        attrs["user"] = user
        return attrs


class CodeLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(phone=attrs["phone"])
        except User.DoesNotExist as exc:
            raise serializers.ValidationError("手机号未注册") from exc

        if attrs["code"] != "123456":
            raise serializers.ValidationError("验证码错误或已失效")

        attrs["user"] = user
        return attrs


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

