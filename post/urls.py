from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>/', views.detail, name='detail'),
    path('logout', views.auth_logout, name='logout'),
               ]