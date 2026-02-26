from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import BorrowRecordViewSet, AddToCartView, RemoveFromCartView, ViewCartView, PlaceBorrowView, BorrowRecordItemsView, CartViewSet, CartItemViewSet



router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'borrow', BorrowRecordViewSet, basename='borrow')
router.register(r'place-borrow', BorrowRecordViewSet, basename='place-borrow')

# Nested router for cart items
cart_router = NestedDefaultRouter(router, r'cart', lookup='cart')
cart_router.register(r'items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', ViewCartView.as_view(), name='view-cart'),
    path('place-borrow/', PlaceBorrowView.as_view(), name='place-borrow'),
    path('place-borrow/<int:borrow_id>/items/', BorrowRecordItemsView.as_view(), name='borrow-items'),
    path('', include(router.urls)),
    path('', include(cart_router.urls)),
]
