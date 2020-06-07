from rest_framework import serializers

from posts.models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date', )
        model = Post
        read_only_fields = ('author', )

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ('author', 'post', 'text', 'created', 'id', )
        model = Comment
        read_only_fields = ('author', )
