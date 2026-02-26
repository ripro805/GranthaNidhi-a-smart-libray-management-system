# =========================
# BORROW RECORD ITEMS VIEW
# =========================
from rest_framework.views import APIView
from .models import BorrowRecord, BorrowRecordItem
from .serializers import BorrowRecordSerializer, BorrowRecordItemSerializer

class BorrowRecordItemsView(APIView):
    def get(self, request, borrow_id):
        borrow_record = get_object_or_404(BorrowRecord, id=borrow_id)
        items = borrow_record.items.all()
        serializer = BorrowRecordItemSerializer(items, many=True)
        return Response(serializer.data)
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import Cart, CartItem, BorrowRecord
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    BorrowRecordSerializer,
)

# =========================
# CART VIEWSET
# =========================
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer


    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            from rest_framework.response import Response
            from rest_framework import status
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer.save(member=self.request.user)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Cart.objects.none()
        return Cart.objects.filter(member=self.request.user)

# =========================
# CART ITEM VIEWSET
# =========================
class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        cart_id = self.kwargs["cart_pk"]
        return CartItem.objects.filter(cart_id=cart_id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

# =========================
# REMOVE FROM CART
# =========================
class RemoveFromCartView(generics.GenericAPIView):
    serializer_class = CartItemSerializer

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        book_id = request.data.get("book_id")
        cart = get_object_or_404(Cart, member=request.user)
        item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
        item.delete()
        return Response({"message": "Book removed from cart"})

# =========================
# VIEW CART
# =========================
class ViewCartView(generics.GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        cart = Cart.objects.filter(member=request.user).first()
        if not cart:
            return Response({"cart": []})
        return Response(self.serializer_class(cart).data)

# =========================
# ADD TO CART
# =========================
class AddToCartView(generics.GenericAPIView):
    serializer_class = AddCartItemSerializer

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        book_id = request.data.get("book_id")
        quantity = int(request.data.get("quantity", 1))
        cart, _ = Cart.objects.get_or_create(member=request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart, book_id=book_id
        )
        item.quantity = item.quantity + quantity if not created else quantity
        item.save()
        return Response({"message": "Book added to cart"}, status=status.HTTP_201_CREATED)

# =========================
# PLACE BORROW
# =========================
class PlaceBorrowView(generics.GenericAPIView):
    serializer_class = BorrowRecordSerializer

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        cart = get_object_or_404(Cart, member=request.user)
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        # Create a single BorrowRecord for this transaction
        borrow_record = BorrowRecord.objects.create(member=request.user)
        items_created = []
        for item in cart.items.all():
            for _ in range(item.quantity):
                bri = BorrowRecordItem.objects.create(
                    borrow_record=borrow_record,
                    book=item.book
                )
                items_created.append(bri)
        cart.items.all().delete()
        return Response({
            "message": "Books borrowed successfully",
            "borrow": BorrowRecordSerializer(borrow_record).data,
            "items": BorrowRecordItemSerializer(items_created, many=True).data
        }, status=status.HTTP_201_CREATED)

# =========================
# BORROW RECORD VIEWSET
# =========================
class BorrowRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRecordSerializer
    queryset = BorrowRecord.objects.all()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return BorrowRecord.objects.none()
        return BorrowRecord.objects.filter(member=self.request.user)
