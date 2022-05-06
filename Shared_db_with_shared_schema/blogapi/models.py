from django.db import models
from tenant.models import TenantAwareModel
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

class blog(TenantAwareModel):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Choice(TenantAwareModel):
    poll = models.ForeignKey(blog, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text


class Reaction(TenantAwareModel):
    choice = models.ForeignKey(Choice, related_name="votes", on_delete=models.CASCADE)
    blog_post = models.ForeignKey(blog, on_delete=models.CASCADE)
    reaction_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("blog_post", "reaction_by")

