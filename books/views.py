from rest_framework import generics

from .models import BookCategory
from .serializers import BookCategorySerializer

# List and detail views for BookCategory
class BookCategoryListView(generics.ListAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer

class BookCategoryDetailView(generics.RetrieveAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, BookReview, BookCategory, BookImage, Author
from .serializers import BookSerializer, BookReviewSerializer, BookCategorySerializer, BookImageSerializer, AuthorSerializer

# Author ViewSet
from rest_framework import viewsets
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
from django.db import models
from .filters import BookFilter, BookReviewFilter
from .pagination import BookResultsSetPagination

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('category').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description', 'category__name', 'author__name']
    ordering_fields = ['avg_rating', 'published_date']
    pagination_class = BookResultsSetPagination

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.annotate(book_count=models.Count('books')).all()
    serializer_class = BookCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    pagination_class = BookResultsSetPagination

class BookImageViewSet(viewsets.ModelViewSet):
    serializer_class = BookImageSerializer
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BookImage.objects.none()
        return BookImage.objects.filter(book_id=self.kwargs['book_pk'])
    def perform_create(self, serializer):
        book_id = self.kwargs['book_pk']
        serializer.save(book_id=book_id)

class AddBookReviewView(APIView):
    def post(self, request, book_id):
        rating = int(request.data.get('rating', 0))
        comment = request.data.get('comment', '')
        if not (1 <= rating <= 5):
            return Response({'error': 'Rating must be between 1 and 5'}, status=400)
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)
        BookReview.objects.create(book=book, reviewer=request.user, rating=rating, comment=comment)
        avg = BookReview.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
        book.avg_rating = avg
        book.save()
        return Response({'message': 'Review added'}, status=201)

class BooksSortedByRatingView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-avg_rating')
    serializer_class = BookSerializer

class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookReviewFilter
    search_fields = ['comment']
    ordering_fields = ['rating', 'created_at']
    def perform_create(self, serializer):
        book_id = self.kwargs['book_pk']
        serializer.save(reviewer=self.request.user, book_id=book_id)
