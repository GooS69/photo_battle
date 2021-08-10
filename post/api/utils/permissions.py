from rest_framework import permissions

from post.my_models.post import Post


class PostPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        if request.method == 'DELETE':
            post = Post.objects.filter(id=view.kwargs['pk']).exists()
            if post:
                return post.owner == request.user
            else:
                return True