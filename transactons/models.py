from django.db import models
from accounts.models import User, MemberProfile
from books.models import Book

# =========================
# CART MODEL
# =========================
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.member.email}"

# =========================
# CART ITEM MODEL
# =========================
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"

# =========================
# BORROW RECORD MODEL
# =========================

# =========================
# BORROW RECORD (Transaction) MODEL
# =========================
class BorrowRecord(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_records')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.email} borrowed on {self.borrow_date}"

# =========================
# BORROW RECORD ITEM MODEL
# =========================
class BorrowRecordItem(models.Model):
    borrow_record = models.ForeignKey(BorrowRecord, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} in borrow {self.borrow_record.id}"
