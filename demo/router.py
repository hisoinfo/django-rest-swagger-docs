
from __future__ import unicode_literals
from rest_framework.routers import DefaultRouter
from rest_framework.routers import Route,DynamicListRoute,DynamicDetailRoute
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

class Router(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{methodname}/{lookup}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
    ]


    def produce_urls(self):
        ret = []
        base_regex = '(?P<{lookup_field}>[^/]+)'

        for prefix, viewset, basename in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:

                # Only actions which actually exist on the viewset will be bound
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                # Build the url pattern
                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    trailing_slash=self.trailing_slash
                )

                if not route.initkwargs:
                    function_name = mapping.get('get', None) or mapping.get('post', None)
                    handler = getattr(viewset, function_name)
                    if hasattr(handler, 'lookup'):
                        lookup_list = []
                        for lp in handler.lookup:
                            lookup_list.append(base_regex.format(lookup_field=lp))
                        custom_lookup = '/'.join(lookup_list)
                        regex = route.url.format(
                                prefix=prefix,
                                lookup=custom_lookup,
                                trailing_slash=self.trailing_slash if custom_lookup else ''
                                )
                view = viewset.as_view(mapping, **route.initkwargs)
                name = route.name.format(basename=basename)
                ret.append(url(regex, view, name=name))
        return ret

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = []

        if self.include_root_view:
            root_url = url(r'^api_root$', self.get_api_root_view(), name=self.root_view_name)
            urls.append(root_url)

        #default_urls = super(DefaultRouter, self).get_urls()
        default_urls = self.produce_urls()
        urls.extend(default_urls)

        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        return urls

#router = Router()
router = DefaultRouter()
router_no_slash = DefaultRouter(trailing_slash=False)
