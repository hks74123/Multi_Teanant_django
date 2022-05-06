from . import views
from django.contrib import admin
from django.urls import path
from .views import LoginView, UserCreate, ChoiceList, BLogViewSet,GiveReaction

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="polls_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/",
        GiveReaction.as_view(),
        name="polls_list",),
    path('all_blogs',views.all_blogs)
]
