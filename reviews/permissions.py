from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsDriverOrClient(BasePermission):
    """
    - Clients can perform any action (CRUD).
    - Drivers can only view (GET) or delete (DELETE) reviews.
    """
    
    def has_permission(self, request, view):
        user = request.user
        client = getattr(user, 'client', None)
        driver = getattr(user, 'driver', None)
        
        # If the user is a client, allow all actions
        if client:
            return True

        # If the user is a driver, allow only GET and DELETE methods
        if driver:
            if request.method in SAFE_METHODS or request.method == 'DELETE':
                return True

        # Deny access for others
        return False
