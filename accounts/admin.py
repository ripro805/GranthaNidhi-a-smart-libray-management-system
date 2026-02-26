

from django.contrib import admin
from .models import User, MemberProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'join_date')
