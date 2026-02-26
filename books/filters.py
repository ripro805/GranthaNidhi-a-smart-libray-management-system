import django_filters
from .models import Book, BookReview

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')
    category__name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    avg_rating = django_filters.RangeFilter(field_name='avg_rating')

    class Meta:
        model = Book
        fields = ['title', 'author', 'category__name', 'avg_rating']

class BookReviewFilter(django_filters.FilterSet):
    class Meta:
        model = BookReview
        fields = {
            'rating': ['gte', 'lte'],
            'reviewer__email': ['icontains'],
            'comment': ['icontains'],
        }
