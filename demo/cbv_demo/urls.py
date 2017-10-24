from django.conf.urls import include, url
from .views import ContactData

from demo.router import router

router.register(r'api-demo', ContactData, base_name='contact')

urlpatterns = [
    # url(r'', include(router.urls))
]