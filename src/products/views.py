from django.shortcuts import render
from django.http import  Http404
# Create your views here.
from django.views.generic import ListView, DetailView
from django.shortcuts import render,  get_object_or_404

from .models import Product

from carts.models import Cart

class ProductFeaturedListView(ListView):
    #queryset= Product.objects.all()
    template_name= "products/list.html"

    def get_queryset(self, **kwargs):
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    queryset= Product.objects.all().featured()
    template_name= "products/featured.html"
    #def get_queryset(self, **kwargs):
    #    request = self.request
    #    return Product.objects.featured()


class ProductListView(ListView):
    #queryset= Product.objects.all()
    template_name= "products/list.html"

    def get_queryset(self, **kwargs):
        request = self.request
        return Product.objects.all()



def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)

class ProductDetailSlugView(DetailView):
    queryset= Product.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug= self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not Found")
        except Product.MultipleObjectsReturned:
            qs = Product.ojects.filter(slug=slug, active=True)
            instance= qs.first()
        except:
            raise Http404("ummmmmmm")
        return instance

class ProductDetailView(DetailView):
    #queryset= Product.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context= super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context
    def get_object(self, *args, **kwargs):
        request = self.request
        pk= self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('Product Dosent exist')
        return instance


    #def get_queryset(self, **kwargs):
    #    request = self.request
    #    pk= self.kwargs.get('pk')
    #    return Product.objects.all()



def product_detail_view(request, pk=None, *args, **kwargs):
    #queryset = Product.objects.all()
    #instance= get_object_or_404(Product, pk=pk)
    #try:
    #    instance = Product.objects.get(id=pk)
    #except Product.DoesNotExist:
    #    print('no product here')
    #    raise Http404('Product Dosent exist')

    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('Product Dosent exist')
    #print(instance)

    #qs = Product.objects.filter(id=pk)
    #if qs.exists() and qs.count() == 1:
    #    instance =qs.first()
    #else:
    #    raise Http404('Product Dosent exist')
    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)
