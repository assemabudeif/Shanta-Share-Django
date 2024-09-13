# reviews/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsDriverOrClient(BasePermission):
    """
    صلاحية مخصصة للسماح للسائقين بمشاهدة المراجعات فقط
    والعميل يمكنه تنفيذ عمليات CRUD.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.user and request.user.is_authenticated:
            if hasattr(request.user, 'driver'):
                return request.method in SAFE_METHODS
            
            if hasattr(request.user, 'client'):
                return True

        return False
