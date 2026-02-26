from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookCategoryViewSet, BookCategoryListView, BookCategoryDetailView

router = DefaultRouter()
router.register(r'categories', BookCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', BookCategoryListView.as_view(), name='category-list'),
    path('<int:pk>/', BookCategoryDetailView.as_view(), name='category-detail'),
]
