from django.contrib import admin
from django.utils.html import format_html

from .models.comment import Comment
from .models.post import Post
from .models.like import Like


@admin.action(description='Mark selected as verified')
def make_verified(modeladmin, request, queryset):
    queryset.update(status='verified')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('name', 'status', 'thumbnail')
    list_editable = ('status', )
    list_filter = ('status',)
    actions = [make_verified]

    @staticmethod
    def thumbnail(obj):
        return format_html('<img src="{}" >'.format(obj.get_img_small_url()))


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


