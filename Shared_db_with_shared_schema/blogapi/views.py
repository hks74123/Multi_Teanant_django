from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth import authenticate

from .models import blog, Choice, Reaction
from .serializers import BlogSerializer, ChoiceSerializer, ReactionSerializer, UserSerializer

from tenant.utils import tenant_from_request
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

class BLogViewSet(viewsets.ModelViewSet):
    queryset = blog.objects.all()
    serializer_class = BlogSerializer

    def get_queryset(self):
        tenant = tenant_from_request(self.request)
        return super().get_queryset().filter(tenant=tenant)

    def destroy(self, request, *args, **kwargs):
        blog = blog.objects.get(pk=self.kwargs["pk"])
        if not request.user == blog.created_by:
            raise PermissionDenied("You can not delete this blog.")
        return super().destroy(request, *args, **kwargs)


class ChoiceList(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset

    def post(self, request, *args, **kwargs):
        blog = blog.objects.get(pk=self.kwargs["pk"])
        if not request.user == blog.created_by:
            raise PermissionDenied("You can not react to this blog.")
        return super().post(request, *args, **kwargs)


class GiveReaction(APIView):
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("reaction_by")
        data = {"choice": choice_pk, "blog_post": pk, "reaction_by": voted_by}
        serializer = ReactionSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

def all_blogs(request):
    MAX_OBJECTS = 20
    blogs = blog.objects.all()[:20]
    data = {
        "results": list(
            blogs.values("pk", "title","content", "created_by__username", "pub_date")
        )
    }
    return JsonResponse(data)


def blog_details(request, pk):
    blog = get_object_or_404(blog, pk=pk)
    data = {
        "results": {
            "title": blog.title,
            "Description": blog.content,
            "created_by": blog.created_by.username,
            "pub_date": blog.pub_date,
        }
    }
    return JsonResponse(data)