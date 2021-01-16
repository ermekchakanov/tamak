from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.relations import SlugRelatedField
from .models import Chief


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

class ChiefSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='first_name', read_only=True)

    def create(self, validated_data):
        if self.context.get('user_id', None):
            validated_data['user_id'] = self.context.get('user_id')
        else:
            validated_data['user_id'] = self.context['request'].user.pk
        return super().create(validated_data)

    class Meta:
        model = Chief
        fields = '__all__'