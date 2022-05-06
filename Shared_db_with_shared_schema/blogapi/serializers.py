from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token 

from .models import blog, Choice, Reaction

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"


class ChoiceSerializer(serializers.ModelSerializer):
    votes = ReactionSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = blog
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"], username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user
