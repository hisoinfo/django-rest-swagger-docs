from django.conf.urls import url, include
from demo.router import router, router_no_slash

try:
    from .swagger_schema import get_swagger_view
except:
    from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='My Demo API')

urlpatterns = [
    url(r'^cbv/', include('demo.cbv_demo.urls')),
    url(r'^fbv/', include('demo.fbv_demo.urls')),
    url(r'^swagger/', schema_view),
]

urlpatterns += [
    url(r'', include(router.urls)),
    url(r'', include(router_no_slash.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
