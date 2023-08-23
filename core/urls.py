from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.user_profiles, name='profiles'),
    path('profile/<str:username>', views.userProfile, name='user_profile'),
    path('profile/<str:username>/follow', views.follow, name='follow'),
    path('profile/<str:username>/unfollow', views.unfollow, name='unfollow'),
    path('like/<int:pk>', views.likePost, name='like_post'),
    path('delete_post/<int:pk>', views.deletePost, name='delete_post'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('account/', views.userAccount, name='account'),    
    path('edit-account/', views.editAccount, name='edit-account'),
    path('upload/', views.upload, name='upload')
    
    
]

