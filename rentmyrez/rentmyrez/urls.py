from listings.views import ListingViewSet
from listings.views import NeighbourhoodViewSet
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.views.generic import TemplateView


resources = [
    'authentication',
    'neighbourhoods',
    'listings'
]

documentation_urls = [
    url(r'^$', type('ApiDocsView', (TemplateView,), dict(get_context_data=lambda self, **_: dict(resources=resources))).as_view(template_name='api-docs/index.html'), name='index')
]

documentation_urls += [
    url(r'^{resource}/$'.format(resource=r), TemplateView.as_view(template_name='api-docs/{resource}.html'.format(resource=r)), name=r)
    for r in resources
]

router = DefaultRouter(schema_title='RentMyRez API')
router.register(r'listings', ListingViewSet)
router.register(r'neighbourhoods', NeighbourhoodViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^api-docs/', include(documentation_urls, namespace='api-docs')),
]
