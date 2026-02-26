from rest_framework import serializers
from .models import User, MemberProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'phone_number', 'role']

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = MemberProfile
        fields = ['id', 'user', 'bio', 'profile_pic', 'social_links', 'join_date']
