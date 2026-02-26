from rest_framework import serializers
from .models import Cart, CartItem, BorrowRecord, BorrowRecordItem
from books.models import Book
from accounts.models import User, MemberProfile

# =========================
# ADD ITEM TO CART
# =========================
class AddCartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity']

    def validate_book_id(self, value):
        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError("Book does not exist")
        return value

    def save(self, **kwargs):
        cart_id = self.context.get('cart_id')
        book_id = self.validated_data['book_id']
        quantity = self.validated_data['quantity']

        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart_id,
            book_id=book_id,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        self.instance = cart_item
        return self.instance

# =========================
# UPDATE CART ITEM
# =========================
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

# =========================
# CART ITEM VIEW SERIALIZER
# =========================
class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity']

# =========================
# CART SERIALIZER
# =========================
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'member', 'items', 'created_at']


# =========================
# BORROW RECORD ITEM SERIALIZER
# =========================
class BorrowRecordItemSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = BorrowRecordItem
        fields = ['id', 'book', 'returned']

# =========================
# BORROW RECORD SERIALIZER
# =========================
class BorrowRecordSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField()
    items = BorrowRecordItemSerializer(many=True, read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ['id', 'member', 'borrow_date', 'return_date', 'items']
