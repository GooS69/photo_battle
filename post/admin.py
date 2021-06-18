from django.contrib import admin

from .models.comment import Comment
from .models.post import Post
from .models.like import Like


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
