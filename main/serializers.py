from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.relations import SlugRelatedField
from .models import Feedback, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        "username"
        "first_name",
        "last_name",
        "email",
        "date_joined",
    )

class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='first_name', read_only=True)

    def create(self, validated_data):
        if self.context.get('author_id', None):
            validated_data['author_id'] = self.context.get('author_id')
        else:
            validated_data['author_id'] = self.context['request'].user.pk
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='first_name', read_only=True)
    comments = CommentSerializer(many=True, required=False)

    def create(self, validated_data):
        if self.context.get('author_id', None):
            validated_data['author_id'] = self.context.get('author_id')
        else:
            validated_data['author_id'] = self.context['request'].user.pk
        return super().create(validated_data)

    class Meta:
        model = Feedback
        fields = (
            'author',
            'feedback_text',
            'date_created',
            'comments',
        )

    

