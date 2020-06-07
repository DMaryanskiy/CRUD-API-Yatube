from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment

class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        if not request.auth:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        queryset = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        queryset = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        queryset = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(queryset, data=request.data, partial=True)
        if queryset.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        queryset = get_object_or_404(Post, id=pk)
        if queryset.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class APICommentList(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        queryset = Comment.objects.filter(post=post)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, post_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APICommentDetail(APIView):
    def get(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        queryset = get_object_or_404(Comment, id=comment_id, post=post)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        queryset = get_object_or_404(Comment, id=comment_id, post=post)
        serializer = CommentSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        queryset = get_object_or_404(Comment, id=comment_id, post=post)
        serializer = CommentSerializer(queryset, data=request.data, partial=True)
        if queryset.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        queryset = get_object_or_404(Comment, id=comment_id, post=post)
        if queryset.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
