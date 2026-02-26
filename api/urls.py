from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from accounts.views import UserViewSet, MemberProfileViewSet
from books.views import BookViewSet, BookCategoryViewSet, BookReviewViewSet, BookImageViewSet

# Main router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', MemberProfileViewSet, basename='profile')
router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', BookCategoryViewSet, basename='category')

# Nested routers for books
books_router = NestedDefaultRouter(router, r'books', lookup='book')
books_router.register(r'reviews', BookReviewViewSet, basename='book-reviews')
books_router.register(r'images', BookImageViewSet, basename='book-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    path('books/', include('books.book_urls')),
    path('categories/', include('books.category_urls')),
    path('accounts/', include('accounts.accounts_urls')),
    path('', include('transactons.transaction_urls')),
]
