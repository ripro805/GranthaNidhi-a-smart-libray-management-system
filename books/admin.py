

from django.contrib import admin
from .models import Book, Author, BookCategory, BookImage, BookReview

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'author', 'category', 'isbn', 'available_copies')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'date_of_birth')

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'description')

@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
	list_display = ('id', 'book', 'image')

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
	list_display = ('id', 'book', 'reviewer', 'rating', 'created_at')
