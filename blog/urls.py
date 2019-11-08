from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostDetail, upvote,downvote
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', PostListView.as_view(), name ='blog-home'),
    path('rest/', views.RestView.as_view(), name='rest'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('post/<int:pk>/', PostDetail, name ='post-detail'),
    path('post/<int:pk>/', PostDetail, name='post-detail'),
    path('post/<int:pk>/upvote/', upvote, name='post-upvote'),
    path('post/<int:pk>/dovote/', downvote, name='post-downvote'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name ='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name ='blog-about'),
]