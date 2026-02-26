
from rest_framework import serializers
from .models import Book, BookCategory, BookImage, BookReview

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ["id", "name", "description"]

class BookImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = BookImage
        fields = ["id", "image"]

class BookSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, read_only=True)
    category = BookCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=BookCategory.objects.all(), source="category", write_only=True)
    class Meta:
        model = Book
        fields = ["id", "title", "author", "description", "avg_rating", "category", "category_id", "isbn", "published_date", "available_copies", "images"]

class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ["id", "book", "reviewer", "rating", "comment", "created_at"]
