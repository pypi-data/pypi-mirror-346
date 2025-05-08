from urllib.parse import urlparse

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def tenant_url(context, view_name, *args, tenant=None, **kwargs):
    """
    Custom template tag to allow for redirects between schemas (ie; for the globalsuperuser dashboard). Django's native urlresolvers strip out subdomains.
    Can be customized for other use cases in the future
    """
    request = context["request"]
    absolute_uri = request.build_absolute_uri(reverse(view_name, args=args, kwargs=kwargs))
    if tenant:
        current_tenant = request.tenant if hasattr(request, "tenant") else None
        parsed_uri = urlparse(absolute_uri)
        constructed_netloc = (
            parsed_uri.netloc.replace(current_tenant, tenant)
            if current_tenant and current_tenant in parsed_uri.netloc
            else f"{tenant}.{parsed_uri.netloc}"
        )
        absolute_uri = f"{parsed_uri.scheme}://{constructed_netloc}{parsed_uri.path}"

    return absolute_uri
