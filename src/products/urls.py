
from django.conf.urls import url
from .views import(
        ProductListView,
        #product_list_view,
        #ProductDetailView,
        #product_detail_view,
        #ProductDetailView,
        #ProductFeaturedListView,
        #ProductFeaturedDetailView,
        ProductDetailSlugView
        )
app_name = 'products'
urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
