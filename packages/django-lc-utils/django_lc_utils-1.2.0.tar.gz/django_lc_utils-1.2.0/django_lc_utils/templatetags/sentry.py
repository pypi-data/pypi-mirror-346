from django import template
from django.conf import settings
from django.db import connection
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def SENTRY_SCRIPTS_INCLUDE():
    html = ""
    if (
        hasattr(settings, "SENTRY_DSN")
        and settings.SENTRY_DSN
        and "https://" in settings.SENTRY_DSN
        and "@" in settings.SENTRY_DSN
    ):
        js_dsn = f"https://js.sentry-cdn.com/{settings.SENTRY_DSN.replace('https://','').split('@')[0]}.min.js"
        html = f'<script src="{js_dsn}" crossorigin="anonymous"></script>'
    return mark_safe(html)  # nosemgrep


@register.simple_tag
def SENTRY_TAGS_INCLUDE(user=None):
    html = ""

    if (
        hasattr(settings, "SENTRY_DSN")
        and settings.SENTRY_DSN
        and "https://" in settings.SENTRY_DSN
        and "@" in settings.SENTRY_DSN
    ):
        release = settings.CODEBUILD_BUILD_NUMBER or "Local-Build"
        base_url = settings.BASE_URL
        commit_id = settings.CODEBUILD_RESOLVED_SOURCE_VERSION or "Local-Build"
        branch_name = settings.CODEBUILD_WEBHOOK_HEAD_REF or "Local-Branch"
        schema = connection.schema_name
        email = user.email if user and user.is_authenticated else ""
        user_id = user.id if user else ""
        username = user.username if user and user.is_authenticated else ""
        schema_user_id = f"{schema}:{user_id}" if schema and user_id else ""
        schema_user_name = f"{schema}:{username}" if schema and username else ""

        html = f"""
    <script>
    Sentry.onLoad(function() {{
        Sentry.init({{
        release: '{release}',
        environment: '{base_url}'
        }});
        Sentry.configureScope(scope => {{
        scope.setTag( 'build_number', '{release}' );
        scope.setTag( 'build_commit', '{commit_id}' );
        scope.setTag( 'build_branch', '{branch_name}' );
        scope.setTag( 'schema', '{schema}' );
        scope.setTag( 'email', '{email}' );
        scope.setTag( 'schema_user_id', '{schema_user_id}' );
        scope.setTag( 'schema_user_name', '{schema_user_name}' );
        }});
    }});
    </script>    """

    return mark_safe(html.replace("\n", " "))  # nosemgrep
