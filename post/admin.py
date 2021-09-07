from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import format_html

from .forms.reject_post_form import RejectPostForm
from .my_models.comment import Comment
from .my_models.post import Post
from .my_models.like import Like

from background_task import background

from .templatetags.post_tags import get_img_url


@background()
def delete_posts(post_id):
    Post.objects.get(id=post_id).delete()


@admin.action(description='Mark selected as verified')
def make_verified(modeladmin, request, queryset):
    queryset.update(status='verified')

@admin.action(description='Mark selected as rejected')
def make_rejected(modeladmin, request, queryset):
    form = None
    if 'apply' in request.POST:
        form = RejectPostForm(request.POST)

        if form.is_valid():
            delay = form.cleaned_data['delete_after'] * 60

            for post in queryset:
                post.status = 'rejected'
                post.save()
                delete_posts(post.id, schedule=delay)

            modeladmin.message_user(request, 'Успешно')
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = RejectPostForm(initial={'_selected_action': request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)})

    return render(request, 'post/admin/reject_post.html', {'items': queryset, 'form': form, 'title': 'Отклонение поста'})

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('name', 'status', 'thumbnail')
    list_editable = ('status', )
    list_filter = ('status',)
    actions = [make_verified, make_rejected]

    @staticmethod
    def thumbnail(obj):
        return format_html('<img src="{}" >'.format(get_img_url(obj, 'small')))


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
