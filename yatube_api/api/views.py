from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


# url из ревью тыкал, там 404
# вот хороший
# https://www.django-rest-framework.org/api-guide/permissions/#permissions
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование только для автора объекта.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
    ]

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        return self.get_post().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
