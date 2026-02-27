from rest_framework import serializers
from .models import User, MemberProfile


from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    first_name = serializers.CharField(required=True, help_text="First name")
    last_name = serializers.CharField(required=True, help_text="Last name")
    address = serializers.CharField(required=True, help_text="Address")
    phone_number = serializers.CharField(required=True, help_text="Phone number")

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'email', 'password', 're_password',
            'first_name', 'last_name', 'address', 'phone_number',
        )
        extra_kwargs = {
            'email': {'required': True, 'help_text': 'Email address'},
            'password': {'write_only': True, 'required': True, 'help_text': 'Password'},
            're_password': {'write_only': True, 'required': True, 'help_text': 'Retype password'},
        }

    def create(self, validated_data):
        validated_data.pop('re_password', None)
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'role']

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = MemberProfile
        fields = ['id', 'user', 'bio', 'profile_pic', 'social_links', 'join_date']
