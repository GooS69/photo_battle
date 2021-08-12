from rest_framework import permissions

from post.my_models.post import Post


class PostPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method in ['POST', 'PUT', 'DELETE']:
            return bool(request.user and request.user.is_authenticated)


class PostsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.query_params.get('preset') == 'user_page':
            return bool(request.user and request.user.is_authenticated)
        return True


class CommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method in ['POST', 'PUT', 'DELETE']:
            return bool(request.user and request.user.is_authenticated)