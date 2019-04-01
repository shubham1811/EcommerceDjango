from django.conf.urls import url
from .views import(
        SearchProductListView,
        )
app_name = 'search'
urlpatterns = [
    url(r'^$', SearchProductListView.as_view(), name='query'),
]

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
