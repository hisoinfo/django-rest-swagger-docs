from django.conf.urls import include, url
from .views import save_medical, get_medical, DemoViewSet
from demo.router import router

router.register(r'finance/demo', DemoViewSet, base_name='testq')

urlpatterns = [
    url(r'^save_medical', save_medical, name='save_contact'),
    url(r'^get_medical', get_medical, name='get_contact'),
]