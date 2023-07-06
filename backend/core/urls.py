from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('signup/', views.sign_up, name='Sign up'),
    path('signin/', views.sign_in, name='Sign in'),
    path('refresh/', views.refresh, name='Refresh tokens'),
    path('getblogs/', views.get_blogs, name='Get blogs'),
    path('getposts/', views.get_posts, name='Get posts'),
    path('createblog/', views.create_blog, name='Create blog'),
    path('addauthor/', views.add_author, name='Add author'),
    path('createpost/', views.create_post, name='Create post'),
    path('createcomment/', views.create_comment, name='Create comment'),
    path('createlike/', views.create_like, name='Create like'),
    path('createsubscription/', views.create_subscription, name='Create subscription'),
    path('getblog/<int:id>/', views.get_blog, name='Get blog'),
    path('getpost/<int:id>/', views.get_post, name='Get post'),
    path('getpostsinblog/<int:id>/<int:n>/', views.get_posts_blog, name='Get posts in blog'),
    path('deleteblog/', views.delete_blog, name='Delete blog'),
    path('deletepost/', views.delete_post, name='Delete post'),
    path('getmyposts/', views.get_my_posts, name='Get my posts'),
    path('getmysubscriptions/', views.get_my_subscriptions, name='Get my subscriptions'),
    path('updatepost/', views.update_post, name='Update post'),
    path('updateblog/', views.update_blog, name='Update blog'),
]