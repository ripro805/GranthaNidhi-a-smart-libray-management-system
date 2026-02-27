
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import User, MemberProfile
from .serializers import UserSerializer, MemberProfileSerializer, CustomUserCreateSerializer

class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer
