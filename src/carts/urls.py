
from django.conf.urls import url
from .views import(
        cart_home,
        cart_update,
        checkout_home,
        checkout_done_view
        )
app_name = 'cart'
urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^checkout/Success/$',checkout_done_view, name='Success'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^update/$', cart_update, name='update'),
]

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
