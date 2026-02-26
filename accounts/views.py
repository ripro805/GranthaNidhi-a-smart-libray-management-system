from rest_framework import viewsets
from .models import User, MemberProfile
from .serializers import UserSerializer, MemberProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer
