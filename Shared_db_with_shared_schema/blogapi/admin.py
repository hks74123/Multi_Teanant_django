from django.contrib import admin
from .models import blog,Choice,Reaction

from django.contrib import admin

from tenant.utils import tenant_from_request

admin.site.register(Choice)
admin.site.register(Reaction)

@admin.register(blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ["title", "content", "created_by", "pub_date"]
    readonly_fields = ["pub_date"]

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        tenant = tenant_from_request(request)
        queryset = queryset.filter(tenant = tenant)
        return queryset

    def save_model(self, request, obj, form, change):
        tenant = tenant_from_request(request)
        obj.tenant = tenant
        super().save_model(request, obj, form, change)

