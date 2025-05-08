from datetime import timedelta

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.utils import timezone
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(ManifestFilesMixin, S3Boto3Storage):
    location = "static"
    bucket_name = getattr(settings, "AWS_STATIC_STORAGE_BUCKET_NAME", None)  # local env breaks w/o this logic
    default_acl = "private"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = "private"
    custom_domain = False

    def url(self, name, parameters=None, expire=None, http_method=None):
        """
        Replace internal domain with custom domain for signed URLs.
        See issue: https://github.com/jschneier/django-storages/issues/165#issuecomment-810166563
        """
        try:
            # put this in a try block for now, so I don't break everything
            from constance import config

            constance_expire = config.AWS_QUERYSTRING_EXPIRE
            url = super().url(name, parameters, constance_expire, http_method)
        except Exception:
            url = super().url(name, parameters, expire, http_method)
        custom_url = url.replace(
            settings.AWS_S3_CUSTOM_DOMAIN,
            f"{settings.AWS_S3_URL_PROTOCOL}//{settings.AWS_S3_CUSTOM_MEDIA_DOMAIN}",
        )
        return custom_url


class PublicMediaRootS3Boto3Storage(S3Boto3Storage):
    bucket_name = "brandings"
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    endpoint_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}"
    default_acl = "private"
    file_overwrite = False
    querystring_auth = False

    def url(self, name, parameters=None, expire=None, http_method=None):
        name = self._normalize_name(self._clean_name(name))
        if expire is None:
            expire = self.querystring_expire

        if self.custom_domain:
            url = "{}/{}/{}".format(settings.AWS_PUBLIC_CLOUDFRONT_DOMAIN, self.bucket_name, filepath_to_uri(name))

            if self.querystring_auth and self.cloudfront_signer:
                expiration = timezone.now() + timedelta(seconds=expire)

                return self.cloudfront_signer.generate_presigned_url(url, date_less_than=expiration)

            return url

        params = parameters.copy() if parameters else {}
        params["Bucket"] = self.bucket.name
        params["Key"] = name
        url = self.bucket.meta.client.generate_presigned_url(
            "get_object", Params=params, ExpiresIn=expire, HttpMethod=http_method
        )
        if self.querystring_auth:
            return url
        return self._strip_signing_parameters(url)


class LocalPublicMediaRootS3Boto3Storage(PublicMediaRootS3Boto3Storage):
    endpoint_url = f"http://{settings.AWS_S3_CUSTOM_DOMAIN}"
