from django.forms import ModelForm

from post.my_models.post import Post


class NewPostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'img']