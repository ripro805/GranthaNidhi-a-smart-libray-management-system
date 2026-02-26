
from django.db import models

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

# Book Category model
class BookCategory(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

# Book model
class Author(models.Model):
	name = models.CharField(max_length=100)
	bio = models.TextField(blank=True)
	date_of_birth = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.name

# Book model
class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
	description = models.TextField(blank=True)
	avg_rating = models.FloatField(default=0)
	category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")
	isbn = models.CharField(max_length=13, unique=True)
	published_date = models.DateField(null=True, blank=True)
	available_copies = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.title

# Book Image model
class BookImage(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="images")
	image = CloudinaryField('image')

# Book Review model
class BookReview(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
	reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.book.title} - {self.rating} by {self.reviewer.username}"



