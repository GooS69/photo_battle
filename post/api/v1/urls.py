from django.urls import path
from .my_views import post_view, like_view, comment_view, post_list_view, comment_list_view

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
    path('post/create', post_view.CreatePostView.as_view()),
    path('post/<int:pk>', post_view.DeletePostView.as_view()),
    path('like', like_view.LikeView.as_view()),
    path('comment', comment_view.CreateComment.as_view()),
    path('post_list/verified_posts', post_list_view.VerifiedPostList.as_view()),
    path('post_list/user_posts', post_list_view.UserPostList.as_view()),
    path('comment_list/post/<int:pk>', comment_list_view.PostComments.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]