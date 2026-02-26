

from django.contrib import admin
from .models import Cart, CartItem, BorrowRecord

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ('id', 'member', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'cart', 'book', 'quantity')

from .models import BorrowRecord, BorrowRecordItem

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
	list_display = ('id', 'member', 'borrow_date', 'return_date', 'items_count')

	def items_count(self, obj):
		return obj.items.count()
	items_count.short_description = 'Books Borrowed'

# Register BorrowRecordItem for completeness
@admin.register(BorrowRecordItem)
class BorrowRecordItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'borrow_record', 'book', 'returned')
