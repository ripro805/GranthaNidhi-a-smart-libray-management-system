from rest_framework import viewsets
from accounts.models import User
from books.models import Book, BookCategory
from transactons.models import Cart, CartItem, BorrowRecord
from accounts.serializers import MemberProfileSerializer
from books.serializers import BookSerializer, BookCategorySerializer
from transactons.serializers import CartSerializer, CartItemSerializer, BorrowRecordSerializer

class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='member')
    serializer_class = MemberProfileSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
