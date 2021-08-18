from django.urls import path
from .my_views import post_view, like_view, comment_view, moderating_view, user_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Photo Battle API",
      default_version='v1',
      description="description",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('posts/', post_view.PostsView.as_view()),
    path('posts/<int:pk>', post_view.PostView.as_view()),
    path('comments/', comment_view.CommentsView.as_view()),
    path('comments/<int:pk>', comment_view.CommentView.as_view()),
    path('like', like_view.LikeView.as_view()),
    path('moderating/post_status/<int:pk>', moderating_view.ChangePostStatus.as_view()),
    path('users', user_view.UsersView.as_view()),
    path('users/<int:pk>/posts', user_view.UserPostsView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]