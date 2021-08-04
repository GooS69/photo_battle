from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('new_post', views.CreateNewPost.as_view(), name='new_post'),
    path('post/<int:pk>', views.DetailPage.as_view(), name='detail_page'),
    path('post/<int:pk>/like', views.CreateLike.as_view(), name='new_like'),
    path('post/<int:pk>/dislike', views.DeleteLike.as_view(), name='delete_like'),
    path('post/<int:pk>/delete', views.DeletePost.as_view(), name='delete_post'),
    path('post/<int:pk>/create_comment', views.CreateComment.as_view(), name='create_comment'),
    path('post/<int:pk>/comments', views.PostComments.as_view(), name='post_comments'),
    path('post/<str:sorting>', views.PostList.as_view(), name='post_list'),
    path('user/<int:pk>', views.UserPage.as_view(), name='user_page'),
    path('user/<int:pk>/change_name', views.UpdateUserName.as_view(), name='change_user_name'),
    path('user/<int:pk>/change_avatar', views.UpdateUserAvatar.as_view(), name='change_user_avatar'),
    path('user/<int:pk>/posts/<str:status>', views.UserPosts.as_view(), name='user_posts'),
    path('user/generate_token', views.GenerateToken.as_view(), name='generate_token'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
    path('api/v1/', include('post.api.v1.urls'))
               ]
