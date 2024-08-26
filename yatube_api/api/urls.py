from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)

post_router = routers.DefaultRouter()
post_router.register('', CommentViewSet, basename='comments')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    re_path(
        r'^posts/(?P<post_id>\d+)/comments/(/(?P<comment_id>\d+)/?)?',
        include(post_router.urls)
    ),
    path('', include(router.urls)),
]
