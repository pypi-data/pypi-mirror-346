from drf_spectacular.openapi import AutoSchema


class LosApiSchema(AutoSchema):
    def get_tags(self):
        from config import api_router, api_router_public

        _tags = ["api"]
        for prefix, viewset, basename in api_router.router.registry:
            if viewset.__name__ == self.view.__class__.__name__:
                _tags.append("tenant")
                break
        for prefix, viewset, basename in api_router_public.router.registry:
            if viewset.__name__ == self.view.__class__.__name__:
                _tags.append("public")
                break

        return _tags
