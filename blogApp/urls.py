
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from .views import *

app_name = 'blogApp'

urlpatterns = [
    path('API/V1', include('blogApp.API.urls')),
    path('', ArticleList.as_view(), name = 'article_list'),
    path('posts/', UnpublishedPosts.as_view(), name = 'article_unpublished'),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('publish/<slug:identifier>', PublishArticle, name = 'article_publish'),    
    path('create/', ArticleCreate.as_view(), name = 'article_create'),
    path('detail/<slug:slug>', ArticleDetail.as_view(), name = 'article_details' ),
    path('delete/<slug:slug>', ArticleDelete.as_view(), name = 'article_delete' ),
    path('update/<slug:slug>', ArticleUpdateView.as_view(), name = 'article_update' ),
    path('comment/<slug:slug>', ArticleCommentView.as_view(), name = 'article_comment' ),
    path('comments/<slug:slug>', CommentDetail.as_view(), name = 'article_comments' ),
    path('comment/delete/<int:pk>', CommentDelete.as_view(), name = 'comment_delete' ),
    path('view/category/<int:pk>', categoryView.as_view(), name = 'category_view' ),

    
    
    
    
    
]