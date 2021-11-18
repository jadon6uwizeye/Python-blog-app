from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import *

urlpatterns = [
    path('', PostList.as_view()),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('unpublished/', UnpublishedPosts.as_view(), name='token_refresh'),    
    path('post/', ArticleCreate.as_view()),
    path('categories/', CategoryView.as_view()),
    path('publish/<slug:identifier>/', PublishView.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('comment/post/', CommentCreateView.as_view()),
    path('comment/<int:pk>/', CommentDetail.as_view()),
]