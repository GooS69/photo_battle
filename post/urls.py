from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.MainPage.as_view(), name='main_page'),
    path('new_post', views.CreateNewPost.as_view(), name='new_post'),
    path('<int:pk>/', views.DetailPage.as_view(), name='detail_page'),
    path('user/<int:pk>', views.UserPage.as_view(), name='user_page'),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),
               ]