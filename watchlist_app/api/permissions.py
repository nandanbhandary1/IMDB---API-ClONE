from rest_framework import permissions


"""Custom Serializer"""
class IsAdminOrReadOnly(permissions.IsAdminUser): # Allow access to only admin user
    def has_permission(self, request, view): # (View-level)
       # 1. admin_permission = bool(request.user and request.user.is_staff) # THIS IS USER IS LOGGED IN AND HE IS AN ADMIN??
        # return request.method == "GET" or admin_permission
        # .2 
       if request.method in permissions.SAFE_METHODS: # GET
            # Check permissions for read-only request 
            return True 
       else:
            # Check permissions for write request
            return bool(request.user and request.user.is_staff) # Check if he's a admin, request.user -> s there a user attached to this request?”
    
    """ if we re logged in as review owner we should have access or it should be get request"""
    
class IsReviewUserOrReadOnly(permissions.BasePermission): # (Object-level)
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request 
            return True 
        else:
            # Check permissions for write request
            return obj.review_user == request.user or request.user.is_staff # one who revied or one who is admin
            