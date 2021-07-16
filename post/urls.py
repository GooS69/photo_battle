from django.urls import path
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
    path('user/<int:pk>', views.UserPage.as_view(), name='user_page'),
    path('user/<int:pk>/change_name', views.UpdateUserName.as_view(), name='change_user_name'),
    #path('user/<int:pk>/change_avatar', views..as_view(), name='change_user_avatar'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
               ]
