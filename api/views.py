from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.urls import reverse

# Create your views here.

@api_view(['GET'])
def api_home(request):
    # Build useful API root links for GranthaNidhi Library
    api_links = {
        "members": request.build_absolute_uri(reverse('member-list')),
        "books": request.build_absolute_uri(reverse('book-list')),
        "categories": request.build_absolute_uri(reverse('category-list')),
        "borrow-records": request.build_absolute_uri(reverse('borrow-list')),
        "carts": request.build_absolute_uri(reverse('cart-list')),
        "cart-items": request.build_absolute_uri(reverse('cartitem-list', kwargs={"cart_pk": 1})),
    }
    return JsonResponse({
        "message": "Welcome to the GranthaNidhi Library API!",
        "links": api_links
    })
