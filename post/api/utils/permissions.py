from rest_framework import permissions

from post.my_models.post import Post


class IsPostOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        post = Post.objects.filter(id=view.kwargs['pk']).exists()
        if post:
            return post.owner == request.user
        else:
            return True
