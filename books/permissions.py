from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsLibrarian(BasePermission):
    """
    Allows access to users with role 'admin', or Django superusers/staff (Librarian).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and (
                getattr(user, 'role', None) == 'admin' or
                getattr(user, 'is_superuser', False) or
                getattr(user, 'is_staff', False)
            )
        )
