from django.http import HttpResponse
from django.shortcuts import render
from django_tenants.utils import remove_www
from tenant.models import Domain
from .models import Article
# Create your views here.
def home(request):

    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    name = domain.tenant.blog_name
    print(name)

    # feature articles on the home page
    featured = Article.articlemanager.filter(featured=True)[0:3]

    context = {
        'name': name,
        'articles': featured
    }

    return HttpResponse(context)