from django.urls import path
from .my_views import post_view, like_view

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
    path('post/create', post_view.CreatePost.as_view()),
    path('post/<int:pk>/delete', post_view.DeletePost.as_view()),
    path('post/list', post_view.PostList.as_view()),
    path('like', like_view.LikeView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]