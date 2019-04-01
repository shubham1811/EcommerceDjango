
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView
from accounts.views import login_page, register_page, guest_register_view
from addresses.views import Checkout_address_create_view, Checkout_address_reuse_view
from .views import home_page, about_page, contact_page
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from carts.views import cart_home
from carts.views import cart_detail_api_view

#from products.views import(
#        ProductListView,
#        product_list_view,
#        ProductDetailView,
#        product_detail_view,
#        ProductDetailView,
#        ProductFeaturedListView,
#        ProductFeaturedDetailView,
#        ProductDetailSlugView
#        )
urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html'), ),
    url(r'^about/$', about_page, name='about'),
    url(r'^login/$', login_page, name='login'),
    url(r'^Checkout/address/create/$', Checkout_address_create_view, name='Checkout_address_create'),
    url(r'^Checkout/address/reuse/$', Checkout_address_reuse_view, name='Checkout_address_reuse'),
    url(r'^register/guest/$', guest_register_view, name='guest_register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/cart$', cart_detail_api_view, name='api-cart'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^register/$', register_page, name='register'),
#    url(r'^featured/$', ProductFeaturedListView.as_view()),
#    url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^search/', include("search.urls", namespace='serach')),
#    url(r'^products-fbv/$', product_list_view),
#    url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
#    url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
#    url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
#    url(r'^cart/$', cart_home, name='cart'),
    url(r'^cart/', include("carts.urls", namespace='cart')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
