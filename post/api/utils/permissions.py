from rest_framework import permissions


class PostsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.query_params.get('preset') == 'user_page':
            return bool(request.user and request.user.is_authenticated)
        return True
