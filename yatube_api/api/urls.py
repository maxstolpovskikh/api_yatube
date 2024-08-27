from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentViewSet, GroupViewSet, PostViewSet

v1_router = routers.DefaultRouter()
v1_router.register('posts', PostViewSet)
v1_router.register('groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_patterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(v1_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
