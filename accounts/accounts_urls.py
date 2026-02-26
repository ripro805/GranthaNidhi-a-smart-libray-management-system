from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MemberProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', MemberProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
