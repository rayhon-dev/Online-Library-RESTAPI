from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'operator'


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user


class IsAdminOrOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'operator']

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.borrower == request.user or request.method in permissions.SAFE_METHODS

class BookPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == 'admin':
            return True
        if user.role == 'operator':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if user.role == 'user':
            if request.method in permissions.SAFE_METHODS:
                return True
            if hasattr(view, 'action') and view.action in ['reserve', 'rate']:
                return True
            return False
        return False



class BookCopyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == 'admin':
            return True
        if user.role == 'operator':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if user.role == 'user':
            return request.method in permissions.SAFE_METHODS
        return False


class GenrePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role == 'admin':
            return True
        if user.role == 'operator':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if user.role == 'user':
            return request.method in permissions.SAFE_METHODS
        return False


class BookLendingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == 'admin':
            return True

        if user.role == 'operator':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

        if user.role == 'user':
            if request.method in permissions.SAFE_METHODS:
                return True
            return False

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role == 'admin':
            return True

        if user.role == 'operator':
            return True

        if user.role == 'user':
            return obj.user == user

        return False

class BookReservationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if view.action == 'overdue':
            return user.role in ['admin', 'operator']

        if user.role == 'admin':
            return True
        if user.role == 'operator':
            return request.method in ['GET', 'PUT', 'PATCH', 'DELETE']
        if user.role == 'user':
            return request.method in ['GET', 'POST']
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'operator':
            return True
        if request.user.role == 'user':
            return obj.reserver == request.user
        return False
