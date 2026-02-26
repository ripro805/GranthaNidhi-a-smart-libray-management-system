from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AddBookReviewView, BooksSortedByRatingView

router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')

urlpatterns = [
    path('sorted/', BooksSortedByRatingView.as_view(), name='books-sorted'),
    path('<int:book_id>/review/', AddBookReviewView.as_view(), name='add-book-review'),
    path('', include(router.urls)),
]
