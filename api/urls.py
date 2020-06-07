from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, APICommentList, APICommentDetail

router = DefaultRouter()
router.register('', PostViewSet, basename='post-list')
router.register('<int:post_id>/', PostViewSet, basename='post-detail')

urlpatterns = [
    path('api/v1/posts/', include(router.urls)),
    path('api/v1/posts/<int:post_id>/comments/', APICommentList.as_view()),
    path('api/v1/posts/<int:post_id>/comments/<int:comment_id>/', APICommentDetail.as_view()),
]

urlpatterns += [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
