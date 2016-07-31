from listings.views import ListingViewSet
from listings.views import NeighbourhoodViewSet
from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'neighbourhoods', NeighbourhoodViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token)
]
