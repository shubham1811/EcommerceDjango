To activate the virtual environment :- .\myenv\activate\Scripts

To run the in local host :- cd src
                            python manage.py runserver
                            
[Complete Database Image 1](https://drive.google.com/open?id=1heqEMT4J_l5UVRA0kuE5l04OccWOM2EI)
[Complete Database Image 2](https://drive.google.com/open?id=1bt7K6zf3aIsbUXCpwp0OOjyjidM7nnJi)
[Product Database Image 1](https://drive.google.com/open?id=1epjTODpniwhT1SQ2EsmY2HfDVFcesc2S)
[Product Database Image 2](https://drive.google.com/open?id=1IBBgDa0iYLlJDy7qto_zOxCz7dnu8cqd)

[Checkout Image 1](https://drive.google.com/open?id=1-HuFUNokW-yaYOWQuRaHaxPFcjBT-cAa)


Explanation of the project:-


*)django-admin startproject projectname
*)in nEW u-> .\myenv\Scripts\activate
*)python manage.py runserver

*)create views.py   ========================================================
*)import
	->from django.http import HttpResponse
	  from django.shortcuts import render
	  def home_page(request):
              return HttpResponse("hello world")

*)url.py ===================================================================
from django.contrib import admin
from django.conf.urls import url
from .views import home_page
urlpatterns = [
    url(r'^$', home_page),   ->as on default the home_page will open
    url(r'^admin/', admin.site.urls),
]

------------------------------------------------------------------------------
For adding the html file 
------------------------------------------------------------------------------
*)make the template folder where the dbsqlite3 is->make the file with .html 
extension.
*)setting.py  ===============================================================
	in template dir add
		->'DIRS': [os.path.join(BASE_DIR, 'templates')],
			tells about the path of the html file
*)view.py     ===============================================================
	def home_page(request):
            return render(request, "home_page.html", {})  ->render home_page.html


-------------------------------------------------------------------------------
For sending dictonaries from view page to the html page
------------------------------------------------------------------------------
*)view.py ===================================================================
	def home_page(request):
    	    context = {   ->dictonaries is defined to send the dict
            "title":"hello shubham welcome to the home page"
            }
    	    return render(request, "home_page.html", context) ->context is pass
	
*)home_page.html ============================================================
	<p>{{title}}</p>   ->data can be printed on the screen


#)bootstrap cdn
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"/>
*)view.py ==================================================================
def contact_page(request):
    context = {
        "title":"hello shubham welcome to the contact page"
    }
    if request.method == "POST":   ->as the form is of post type
        print(request.POST)        ->to get dictionaries of data
        print(request.POST.get('fullname))    ->to get value of the full name
    return render(request, "contact/view.html", context)


-----------------------------------------------------------------------------
for Form
-----------------------------------------------------------------------------
rightclick->new file ->form.py

*)form.py ====================================================================

from django import forms

class ContactForm(forms.Form):
    fullname = forms.CharField( widget =forms.TextInput(attrs={"class": "form-control","placeholder":"your name"}))
    email = forms.EmailField( widget =forms.EmailInput(attrs={"class": "form-control","placeholder":"Your email"}))
    content = forms.CharField(widget =forms.Textarea(attrs={"class": "form-control","placeholder":"Your message"}))

widget can be searched in the google

*)views.py ============================================================================================

from .forms import ContactForm
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"hello shubham welcome to the contact page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, "contact/view.html", context) 

-----------------------------------------------------------------------------
For dbsqlite3
-----------------------------------------------------------------------------
*)python manage.py migrate
*)python manage.py createsuperuser
	shubham
	apna password

------------------------------------------------------------------------------
For login page
------------------------------------------------------------------------------
#)View.py=====================================================================

def login_page(request):
    form = LoginForm(request.POST or None) ->loading the content of login form
    context ={
        "form": form       ->sending as the dictionary
    }
    print("User logged in")     
    #print(request.user.is_authenticated())
    if form.is_valid(): ->it is user defined function and is always false at the first 
        print(form.cleaned_data)  ->print username and password
        username = form.cleaned_data.get("username")  ->getting data from cleadned_data username
        password = form.cleaned_data.get("password")  ->getting data from cleaned_data password
        user = authenticate(request, username=username, password=password) ->if password and the username is true than it give the value of the user
        print(user)    ->the user is printed
        #print(int(request.user.is_authenticated()))
        if user is not None:  ->if authenticated user contain username
            #print(request.user.is_authenticated())
            login(request, user)  ->login the user
            # Redirect to a success page.
            #context['form'] = LoginForm
            return redirect("/login")  ->open again the login page
        else:
            # Return an 'invalid login' error message.
            print("error")      ->something error as occured
    return render(request, "auth/login.html", context)  ->render the page login.html


-----------------------------------------------------------------------------
for register
-----------------------------------------------------------------------------
*)View.py ===================================================================
from django.contrib.auth import authenticate, login, get_user_model
user = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context={
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = user.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "auth/register.html", context)
*)form.py ====================================================================

from django.contrib.auth import get_user_model
User = get_user_model()
class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField( widget =forms.EmailInput)
    password = forms.CharField( widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username taken")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return data
-----------------------------------------------------------------------------
for setting the static file/load into server/load css
-----------------------------------------------------------------------------
*)Setting.py=================================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_proj"), to load the  css file
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")->to load all the file in static_cdn that can be loaded in server
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "media_root")->to load the media file  in ststic_cdn that can be loaded in server
MEDIA_URL = '/media/'

*)url.py ====================================================================

from django.conf import settings
from django.conf.urls.static import static

*)in command prompt run->python manage.py collectstatic

*)home_page.html============================================================

{% load static %}
<link rel='stylesheet' href='{% static "css/main.css" %}'/>
<img src="{% static 'img/beach.jpg'%}" class="img-fluid" />

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
FOLDERS
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

*)create the static_cdn where the src folder is their->create media_root

*)craete the static_my_proj in src where the dbsqlite3 is their->create css->main.css->img->beach.jpg

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
To create the app
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
*)go the src directory in cmd type->python manage.py startapp appname

-----------------------------------------------------------------------------
#)CRUD
-----------------------------------------------------------------------------

*)create  --post
*)REtrieve/List/Search -- get
*)update --Put/ Patch/ Post
*)Delete --Delete

Every app or website using the crud 

-----------------------------------------------------------------------------
for Database
-----------------------------------------------------------------------------
#)Models.py

class Product(models.Model):   ->table name 
    title   =models.CharField(max_length=120)  ->column name
    description = models.TextField()  ->column name 
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)

    def __str__(self):
        return self.title    ->print in the admin the title 

#)setting.py of the ecommerce

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #our application
    'products',           ->here we have to assign the table name
]

#)admin.py

# Register your models here.
from .models import Product   ->for importing the database
admin.site.register(Product)


*)python manage.py makemigrations
*)python manage.py migrate



----------------------------------------------------------------------------
For viewing of the products
----------------------------------------------------------------------------

#)view.py of the products

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.shortcuts import render

from .models import Product

class ProductListView(ListView):         ->class view
    queryset= Product.objects.all()      ->irritate through hole database 
    template_name= "products/list.html"  ->template name


def product_list_view(request):          ->Function view     
    queryset = Product.objects.all()     ->irritate through hole database
    context = {                          ->dictionary 
        'object_list': queryset
    }
    return render(request, "products/list.html", context)  ->calling tempplate and passing the value

*)creating the template folder

products folder mai ->templates->products->list.html

*)Designing the templates

#)list.html

{% for obj in object_list %}  ->as the obhect_list is dicionatry

{{ obj.title }} <br/>         ->printing the title

{% endfor  %}                 ->ending the loop


*)creating the urls

from products.views import ProductListView, product_list_view

url(r'^products/$', ProductListView.as_view()),
url(r'^products-fbv/$', product_list_view),

-----------------------------------------------------------------------------
Detail View
-----------------------------------------------------------------------------
#)view.ppy

class ProductDetailView(DetailView):  ->defining the class as Detail view
    queryset= Product.objects.all()   ->quueryset is must it will contain all the data of the database
    template_name= "products/detail.html"  ->to create template

    def get_context_data(self, *args, **kwargs):  ->To get the  value
        context= super(ProductDetailView, self).get_context_data(*args, **kwargs) ->it just like  creating the dictionary
        return context ->return too the template page


def product_detail_view(request, pk=None, *args, **kwargs): ->
    #queryset = Product.objects.all()
    instance= get_object_or_404(Product, pk=pk)
    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)


-----------------------------------------------------------------------------
For uploading the image file
----------------------------------------------------------------------------

#)Model.py

from django.db import models   ->for using the database
import random                  ->for bringing the new random number
import os		       ->as the know the file used in the static cdn
# Create your models here.

def get_filename_ext(filepath):   ->user defined function takes the argument filepath
    base_name = os.path.basename(filepath)  ->take the filename in the file path
    name,ext = os.path.splitext(base_name)  ->slit the base name in filename and the extension
    return name, ext   ->return the extension and filename

def upload_image_path(instance, filename): -> takes the instance as the title name send  from the view.py filename is the name of the imagge file 
    #print(instance) -> print the  name of the title  (print here as the t-shirt)
    #print(filename) ->print the fiilename
    new_filename = random.randint(1,876357186287)   ->create the randoom number between the 1 and ----  and it go to new_filename
    name, ext = get_filename_ext(filename)   ->calling the function get_filename_ext and that function returns the extension and the name of the  file 
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )
class Product(models.Model):
    title   =models.CharField(max_length=120)
    description = models.TextField()
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image =models.ImageField(upload_to=upload_image_path, null=True, blank=True)  ->creating the table to save the image
    def __str__(self):
        return self.title


class Product(models.Model):
    title   =models.CharField(max_length=120)
    description = models.TextField()
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image =models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    def __str__(self):
        return self.title


#)detail.py

<img src='{{object.image.url}}' class="img-fluid" /> ->print the image 


------------------------------------------------------------------------------
SlugField
------------------------------------------------------------------------------
This field is used to change the url we can search it by the product name.

#)Models.py
Class Products(models.Model):
	slug   =models.SlugField(blank=True, unique=True) ->unique so that it will contain all the slug of different value 

#)Admin.py
class ProductAdmin(admin.ModelAdmin):->  defining the class
    list_display = ['__str__','slug']->  creating the list and printin the slug in the admin pannel
    class Meta:
        model = Product

#)view.py
class ProductDetailSlugView(DetailView): -> creating the class with DetailView as  the function
    queryset= Product.objects.all()  ->query set is must it will contain all the element of the database
    template_name= "products/detail.html"

#)url.py

url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),

	we can search it using the slug


url:-https://www.codingforentrepreneurs.com/blog/common-regular-expressions-for-django-urls/

-----------------------------------------------------------------------------
Random Slug Generator
-----------------------------------------------------------------------------

create the file in products

#)utils.py
import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


#)models.py

from django.db.models.signals import pre_save, post_save ->so that the first the utils.py will run
from .utils import unique_slug_generator  ->calling the utils.py

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)

-----------------------------------------------------------------------------
Reducing the urls
-----------------------------------------------------------------------------
craete the new file in product ->urls.py

copy pasted  all the urls of the ecommerce

urls.py  ->products



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
urlpatterns = [
    url(r'^$', ProductListView.as_view()), 
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
]

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urls.py ->ecommerce


from django.contrib import admin
from django.conf.urls import url, include  ->(include is imported so that urls.py of the products can be imported)
from .views import home_page, about_page, contact_page, login_page ,register_page
from django.conf import settings
from django.conf.urls.static import static
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
    url(r'^$', home_page),
    url(r'^about/$', about_page),
    url(r'^login/$', login_page),
    url(r'^contact/$', contact_page),
    url(r'^register/$', register_page),
#    url(r'^featured/$', ProductFeaturedListView.as_view()),
#    url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    url(r'^products/', include("products.urls")), ->calling the urls.py of the product
#    url(r'^products-fbv/$', product_list_view),
#    url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
#    url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
#    url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#Models.py
class Product(models.Model):
	def get_absolute_url(self):
        return "/products/{slug}/".format( slug=self.slug )

#list.html

{% for obj in object_list %}

<a href='{{ obj.get_absolute_url }}'>{{ obj.title }} </a> <br/> ->calling the the file when pressed on it. 

{% endfor  %}


working
@)url entered by the user->url ecommerce ->url product->view.py->list.hyml->models.py->another page

-----------------------------------------------------------------------------
spliting the html code
-----------------------------------------------------------------------------
*)create the file in template of the ecommerce ->base.html

#base.html

{% load static %}->to load the css file and the image as they are in the static folder
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% include 'base/css.html'%} ->to include the bootstrap file and css file
    {% block base_head %}{% endblock %} ->to include main.css that is included in the homepage
    <title>Bootstrap 101 Template</title>
  </head>
  <body>
    {% block content %}{% endblock %} ->to print the block that are in the between them

    {% include 'base/navbar.html' %} ->to inherit the feature

    {% include 'base/js.html' %} ->to inherit the feature
  </body>
</html>

#)create the folder base in the template 
	#)create the file css.html and js.html and navbbar.html in the base folder

#)css.html
{% load static %}
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"/>

#)js.html

{% load static %}
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"/>

#)view.html
{% extends "base.html" %} ->extending the base.html
{% load static %}
{% block content %}        ->block with name content
    </head>
    <body>
      <h1>Hello, world!</h1>
      <div class="container">
        <div class="row">
          <div class="col">
            <p>{{title}}</p>
            <form method='POST'>{% csrf_token %}
              {{form}}
              <button type="submit" class="btn btn-danger">Submit</button>
            </form>
          </div>
        </div>
      </div>
{% endblock %}   ->endblock


#)home_page.html

{% extends "base.html" %}
{% load static %}
{% block base_head %}  ->calling the main.css
 <link rel='stylesheet' href='{% static "css/main.css" %}'>
{% endblock %}
{% block content %}
    <div class="text-center tex">
      <h1>Hello, world! we are working</h1>
    </div>
    <div class="container">
      <div class="row">
        <div class="col">
          <img src="{% static 'img/beach.jpg'%}" class="img-fluid" />
          <p>{{content}}</p>
        </div>

      </div>
      {% if request.user.is_authenticated %}
      <div class="row">
        <div class="col">
          <h1>Premium</h1>
          <p>{{premium_content}}
        </div>
      </div>
      {% endif %}
    </div>
{% endblock %}

-----------------------------------------------------------------------------
For sending the data from one html file to another
-----------------------------------------------------------------------------

*)we are calling the navbar.html from base.html and we are sending data from
	base.html to navbar.html

#)base.html

{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {% include 'base/css.html'%}
    {% block base_head %}{% endblock %}
    <title>Bootstrap 101 Template</title>
  </head>
  <body>
    {% block content %}{% endblock %}

    {% include 'base/navbar.html' with brand_name='eCommerce'  %}  ->from here we are sending the data to navbar.html as the brand_name.

    {% include 'base/js.html' %}
  </body>
</html>

#)Navbar.html

<h1>{{brand_name}}</h1> here we are getting the brand_name and we are printing that

-----------------------------------------------------------------------------
Adding card to page
-----------------------------------------------------------------------------
#)products->template->products
	create the new folder snippets
		create the new file card.html



#)list.html

{% extends "base.html" %} ->extending thee base.html
{% block content %}       ->creating the block that can be inherited
  <div class="container">
    <div class="row">
  {% for obj in object_list %} ->the Object_list contain all the value from the dataset
  <div class="col">
    {% include 'products/snippets/card.html' with instance=obj %} ->calling the card.html and passing the obj as the instance to the card.html
  </div>
</div>
</div>
  {% endfor  %}
{% endblock %}


#)card.html

<div class="card" style="width: 18rem;">
  {% if instance.image %} ->instance containg the dataset 
    <a href="{{instance.get_absolute_url}}"> ->when clicked on image it will show the detail page
      <img class="card-img-top" src=" {{ instance.image.url }}" alt="Card image cap">  ->show the image
    </a>
  {% endif %}
  <div class="card-body">
    <h5 class="card-title">{{ instance.title }}</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    <a href="{{instance.get_absolute_url}}" class="btn btn-primary">View</a>
    <!--<a href="{% url 'products:detail' slug=instance.slug %}" class="btn btn-warning">URL</a> -->
  </div>
</div>

@@@@@@ WORKING @@@@@@@@@@@@@@@@@@@@

url.py(ecommerce)->url.py(products)->view.py(products)->return the object_list
 to the list.html ->send the instance to the  card.html

Anything that is return as return Product.objects.all()

returned as the object_list

-----------------------------------------------------------------------------
Reversing the url
-----------------------------------------------------------------------------
if the url include the same url.py than by the use of the namespace we can 
differ them

-----------------------------------------------------------------------------
Navbar  Adding the url to the navbar content
-----------------------------------------------------------------------------
#)navbar.html

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">{% if brand_name %} {{brand_name}} {% else %} CFE ecommerce{% endif %}</a> the data is send from the base.html if it contain some data than it will print the data and otherwise if it dosent contaiin than it will print the another data 
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="{% url 'home' %}">Home <span class="sr-only">(current)</span></a> ->here the href contain the url that on clicked it takes to that page and name is given from the url.py of the products
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Contact</a>
      </li>
      <li class="nav-item">
        <a class="nav-link " href="#">product</a>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>


-----------------------------------------------------------------------------
Truncate the title or linebreak Time
-----------------------------------------------------------------------------
#)card.html

<div class="card" style="width: 18rem;">
  {% if instance.image %}
    <a href="{{instance.get_absolute_url}}">
      <img class="card-img-top" src=" {{ instance.image.url }}" alt="Card image cap">
    </a>
  {% endif %}
  <div class="card-body">
    <h5 class="card-title">{{ instance.title }}</h5>
    <p class="card-text">{{ instance.description| truncatewords:3 }}</p>  ->only 3 word will be shown on the screen and than dots will be their
    <a href="{{instance.get_absolute_url}}" class="btn btn-primary">View</a>
    <!--<a href="{% url 'products:detail' slug=instance.slug %}" class="btn btn-warning">URL</a> -->
  </div>
</div>
#)models.py

class Product(models.Model):
    title   =models.CharField(max_length=120)
    slug   =models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image =models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured =models.BooleanField(default=False)
    active =models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True) ->contains the current time
    
    objects = ProductManager()

#)detail.html

{% extends "base.html" %}
{% block content %}
<div class="container">
  <div class="row">
    <div class="col>"
      <h3>{{ object.title }} <br/></h3>
      {{ object.timestamp }}
      {{ object.description|linebreaks }} <br/>  ->break the line
      {{ object.timestamp }}  ->print the current time
      {% if object.image %}
        <img src='{{object.image.url}}' class="img-fluid" />
      {% endif %}
      {% endblock %}
    </div>
  </div>
</div>



{{ forloop.counter }}  ->count the total product starting with 0 and print to the screen


-----------------------------------------------------------------------------
Adding bootstrap to the  site
-----------------------------------------------------------------------------
ecommerce->template->create the folder
		->bootstrap->example.html

#)url.py

from django.views.generic import TemplateView  ->as the tempate is called diretly

url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html'), ),


->url is given the template_name ->location of the file

container in bootstrap it will cover the less space or some column

container-fluid cover the full column


-----------------------------------------------------------------------------
For creating the search box or searching in the list
-----------------------------------------------------------------------------
in src create the new project app

#)python manage.py startapp search

add it to  the setting.py search 


http://127.0.0.1:8000/search/?q=shirt

-----------------------------------------------------------------------------
A Basic search view
-----------------------------------------------------------------------------

*)url.py ->ecommerce

    url(r'^search/', include("search.urls", namespace='serach')),

*)url.py  ->search
    from django.conf.urls import url
    from .views import(
        SearchProductListView,
    )
    app_name = 'search'
    urlpatterns = [
    url(r'^$', SearchProductListView.as_view(), name='query'), ->as the name is given and in view the function is called
]

*)view.py -Search

from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
# Create your views here.
class SearchProductListView(ListView): ->function name
    template_name= "search/view.html"  ->template name 

    def get_context_data(self, *args, **kwargs):
        context= super(SearchProductListView,self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        #SearchQuery.objects.create(query=query)
        return context



    def get_queryset(self, **kwargs):
        request = self.request
        print(request.GET)
        method_dict = request.GET
        query = method_dict.get('q')
        if query is not None:
            return Product.objects.filter(title__icontains=query) returned as the object_list
        return Product.objects.featured()


#)view.html

{% extends "base.html" %}
{% block content %}
  <div class="container">
    <div class="row" mb-3>
      {% if query %} ->as it receive the context as the argument as the query contain the item that is to be searched
      <div class="col-12 mb-3">
        Result for<b> {{ query }}</b> ->print the query
      </hr>
      </div>
      {% else %}  ->If the query set  dosent contain anything
        <div class="col-12 col-md-8 mx-auto py-2">
            {% include 'search/snippets/search-form.html' %}   ->call the search form
        </div>
        {% endif %}
        <div class="col-12">
          <hr>
        </div>
  </div>
  <div class="row">

    {% for obj in object_list %}
    <div class="col">
      {% include 'products/snippets/card.html' with instance=obj %}
      {% if forloop.counter|divisibleby:3 %}
    </div></div><div class="row"><div class="col-12"><hr/></div>
      {% elif forloop.counter|divisibleby:2 %}
    </div></div><div class="row"><div class="col-12"><hr/></div>

      {% else %}
        </div>
      {% endif %}
    {% endfor  %}
</div>
</div>
{% endblock %}

#)Search ->create the new folder(snippets)->create the file(search-form.html)

	#)search-form.html

<form method="GET" action='{% url "search:query" %}' class="form my-2 my-lg-0"> when the form is submitted the url is called the namespace search and the name query is called and the q is passed
  <div class="input-group">
  <input class="form-control" type="search" placeholder="Search" name="q" value="{{ request.GET.q }}" aria-label="Search"/> whatever will be typed in input box will be stored in the name q and the input box will contain the value
  <span class="input-group-btn"/>
    <button class="btn btn-outline-success my-sm-0" type="submit">Search</button>
  </span>
</div>
</form>

@@@@@)the snippets is added to the navbar.html of the ecommerce

	  {% include 'search/snippets/search-form.html' %}


-----------------------------------------------------------------------------
For searching throug the keyword
-----------------------------------------------------------------------------
#)views.py

    def get_queryset(self, **kwargs):
        request = self.request
        print(request.GET)
        method_dict = request.GET
        query = method_dict.get('q')
        if query is not None:
            return Product.objects.search(query)-> called the search function in the model.py and the as argument query is passed
        return Product.objects.featured()


#)models.py  ->products

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True, active=True)
    def Search(self, query): ->this is called by the ProductManager
        lookups = (Q(title__icontains=query) | it searches if the title contain the query or not
                  Q(description__icontains = query)|
                  Q(price__icontains=query))
        return self.filter(lookups).distinct() ->return the didtinct query set
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    def all(self):
        return self.get_queryset().active()
    def featured(self):
        return self.get_queryset().featured()
    def search(self, query):   ->it is called by the views.py
        return self.get_queryset().active().Search(query) ->it will call the Search 
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


-----------------------------------------------------------------------------
Search by different Tag name
-----------------------------------------------------------------------------
#)create the new app

src->python manage.py startapp tags

#)models.py   ->tags
	As it is made beacuse we can use the the product model as a foriegn key
and we can add the title and discription to the products.

from django.db import models
from django.db.models.signals import pre_save, post_save ->for generating the slug
from products.utils import unique_slug_generator ->for slug
from products.models import Product  ->importing the products model
# Create your models here.
class Tag(models.Model):  ->Model name
    title = models.CharField(max_length=120)  ->creating the title name
    slug = models.SlugField()  ->creating the slug field
    timestamp = models.DateTimeField(auto_now_add = True) ->creating the time field
    active = models.BooleanField(default=True)->creating the active field
    products = models.ManyToManyField(Product, blank=True)
	->importing all the field of the model of the products as the foriegn key
		
    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs): ->forcenerating the slug
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(tag_pre_save_receiver, sender=Product)


#)admin.py  ->tags

from django.contrib import admin

# Register your models here.
from .models import Tag   ->for importing the tag model

admin.site.register(Tag)  ->for showing that in the admin pannel

#@@@@@@)  add the tags to the setting of the ecommerce

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True, active=True)
    def Search(self, query):
        lookups = (Q(title__icontains=query) |
                  Q(description__icontains = query)|
                  Q(price__icontains=query) |
                  Q(tag__title__icontains=query))
			
			tag is model name and title is entity name


-----------------------------------------------------------------------------
Create the cart
-----------------------------------------------------------------------------

create the new app Cart
*)python manage.py startapp Cart

url.py (ecommerce)

from carts.views import cart_home
url(r'^cart/$', cart_home, name='cart'),

if any urls is included in the url than we dont have to import

Models.py (Cart)

from django.db import models
from django.conf import settings
from products.models import Product  ->to import the product model that can be used as the foriegn key

User = settings.AUTH_USER_MODEL  ->getting the user name and other sttuff of the user

class Cart(models.Model):  creating the database
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  ->creating the foreign key that can be used in the another database
    products =models.ManyToManyField(Product, blank=True) many product can be added 
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2) for adding the items in the cart
    updated = models.DateTimeField(auto_now=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)

#)View.py(Cart)

from django.shortcuts import render
from .models import Cart
# Create your views here.
def cart_create(user=None):   a function is created that create the new cart
    cart_obj = Cart.objects.create(user=None) ->create the cart
    print("new cart created") ->print that new cart has been created
    return cart_obj   ->return the object
def cart_home(request):
    request.session['cart_id'] = "12"  ->created the default cart_id as it is created because if the user is not login he can also add to the cart and its items cant be go out from the cart
    cart_id = request.session.get("cart_id", None) ->if for the user the cart_id is their than it will get otherwise it will none
    qs = Cart.objects.filter(id=cart_id)   ->it will filter yjeid
    if  qs.count() == 1:  ->
        print('cart id exists')
        cart_obj = qs.first()
    else:
        cart_obj = cart_create()
        request.session['cart_id'] = cart_obj.id
    return render(request, "carts/home.html", {})

create the new fldor for html

templates->carts->home.html

@@@@@@@@@)changing the template


#)admin.py

from django.shortcuts import render
from .models import Cart
# Create your views here.

def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request) calling the function of the model and taking the return 
    return render(request, "carts/home.html", {}) ->rendering the page home.html

#)MOdels.py

from django.db import models
from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL  ->taking the user name 

class CartManager(models.Manager):
    def new_or_get(self, request):   ->creating the function 
        cart_id = request.session.get("cart_id", None) ->if the cart_id is their than the it will get the id or therwise the none 
        qs = self.get_queryset().filter(id=cart_id) -> if the cart_is is their than it will filter that id
        if  qs.count() == 1: ->if qs has any value than than it will be 1
            new_obj=False  ->as new cart is not created thats why false
            cart_obj = qs.first()   ->get the first id
            if request.user.is_authenticated and cart_obj.user is None:  ->if user is logout and it add something to the cart that time and after adding it log in to the cart than that time user is authenticated and user_obj is none 
                cart_obj.user = request.user   ->reqest for the user
                cart_obj.save()  ->save to the database

        else:
            cart_obj = Cart.objects.new(user=request.user)  create the new user
            new_obj = True  ->as the new cart is made thats why true
            request.session['cart_id'] = cart_obj.id  ->creating the new cart_is for that time
        return cart_obj, new_obj ->returing the cart_obj, new_obj
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products =models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()
    def __str__(self):
        return str(self.id)

=============================================================================
changing the cart
=============================================================================

#view.py(Cart)

from django.shortcuts import render
from .models import Cart
# Create your views here.

def cart_home(request):
    return render(request, "carts/home.html", {})


#Models.py

from django.db import models
from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed ->this is imported so that while saving the total changes
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if  qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj   ->cart_obj return the user id
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products =models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()
    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance ,action, *args, **kwargs):  
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':  ->as something is changed or something is saved
        products = instance.products.all() ->get the all the products that it is having
        total = 0
        for x in products:  ->counting from 1 to product
            total += x.price  ->adding the price
        if instance.subtotal != total:  ->if both are not equal
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)  ->sender is that because products is manytomany

def pre_save_cart_receiver(sender, instance , *args, **kwargs):
    instance.total = instance.subtotal   ->saving the subtototal the instance

pre_save.connect(pre_save_cart_receiver, sender=Cart)


------------------------------------------------------------------------------
Adding to the cart
-------------------------------------------------------------------------------

++)urls.py (ecommerce)

    url(r'^cart/', include("carts.urls", namespace='cart')),

++)urls.py(cart)
 
from django.conf.urls import url
from .views import(
        cart_home,
        cart_update,
        )
app_name = 'cart'
urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^update/$', cart_update, name='update'),
]

++)view.py(cart)

def cart_update(request):
    product_id = 1 assigning the product id
    product_obj = Product.objects.get(id = product_id) getting title of product 1
    cart_obj, new_obj = Cart.objects.new_or_get(request) ->getting the cart_obj(id) and new_obj(cart newely created or old one)
    if product_obj in cart_obj.products.all(): ->
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    return redirect("cart:home") ->redirect to namespace cart and name home


++)view.py(Products)

class ProductDetailSlugView(DetailView):
    queryset= Product.objects.all()
    template_name= "products/detail.html"

    def get_context_data(self, *args, **kwargs): return the dictionary
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj ->Cart_obj contain the id 
        return context  ->return dictionary to the page

++)detail.html

<div class='col-12 col-md-6'>
      {% if object in cart.products.all %} ->checking that the object is in the cart or not if it is their that remove button comes
        In cart<button class="btn btn-link">Remove</button>
      {% else %}
        In cart<button class="btn btn-success">Add to cart</button>
      {% endif %}
  </div>

-----------------------------------------------------------------------------
Adding to the cart database
-----------------------------------------------------------------------------
from decimal import Decimal
from django.db import models
from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed
User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if  qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products =models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CartManager()
    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance ,action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance , *args, **kwargs):
    if instance.subtotal:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08)
    else:
        instance.total = 0.00
pre_save.connect(pre_save_cart_receiver, sender=Cart)
-----------------------------------------------------------------------------
Adding the  cart look 
-----------------------------------------------------------------------------
##))view.py


from django.shortcuts import render, redirect
from .models import Cart
from orders.models import Order
from products.models import Product
from orders.models import Order
# Create your views here.

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, "carts/checkout.html", {"object": order_obj})


-----------------------------------------------------------------------------
working till  now
-----------------------------------------------------------------------------
##)ecommerce url.py
url(r'^cart/', include("carts.urls", namespace='cart')), ->including the url.py of the cart wit the namespace cart

##)cart url.py
app_name = 'cart'
urlpatterns = [
    url(r'^$', cart_home, name='home'), ->for opening the cart page where it contain the prduct item puted in the cart
    url(r'^checkout/$', checkout_home, name='checkout'), ->for the checkoutt the order
    url(r'^update/$', cart_update, name='update'),
]

##)view.py cart
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj}) sending the cart to the html page

##)models.py Cart

def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if  qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

##)view.py Cart

for cart_upadate for removing or adding the product

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")


-----------------------------------------------------------------------------
Working through the product list and adding to he cart  flow
-----------------------------------------------------------------------------
#))view.py product->render the page list.html ->render the page card.html ->go to the model.py of the
product ->render the detail.py ->render the card-update.html ->
from there the product is send to the cart ->update with the name product_id 
having the value product.id->their it operate add or remove the product
and redirect the page cart->home

-----------------------------------------------------------------------------
craeting the order app
-----------------------------------------------------------------------------
$$)python manage.py startapp oders


**)Models.py
from django.db import models
import math


# Create your models here.
from carts.models import Cart  ->importing the cart Models.py
from ecommerce.utils import unique_order_id_generator ->import unique random string generatoor from the ecommerce
from django.db.models.signals import pre_save, post_save  ->for the operation when the button is clicked for the pre save and post save

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),                ->for creating the dictionary
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)
class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)  ->Saving the random order_id generator
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)   ->work as the foreignn key where we can use the every entity of the cart
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)  ->choices that initialized in the dictionary
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)  -if the shopping total is  their  it will be their in the entity
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)  ->adding all the table entity

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total ->updating the cart_total to the cart total value
        shipping_total = self.shipping_total  ->getting the shipping_total from the database and puting to tha variable
        new_total = math.fsum([cart_total,shipping_total]) ->adding both the valuse and converting oit to fsum
        formatted_total = format(new_total, '.2f')  ->converting model to the 2 point after the decimal
        self.total = formatted_total  ->puting the value to tha database
        self.save()
        return new_total
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:   ->if oder_is is none 
        instance.order_id = unique_order_id_generator(instance)  ->calling the function from eccommerce and  initializing the value
pre_save.connect(pre_save_create_order_id, sender=Order) ->as the value to the function is send  by the sender

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        print("Error")
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created,*args, **kwargs):
    print("running")
    if created:
        print("updating.. first")
        instance.update_total()  ->calling the funnction update 
post_save.connect(post_save_order, sender=Order)

-----------------------------------------------------------------------------
viewing the checkout page
-----------------------------------------------------------------------------

##)view.py  cart

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)  ->getting the cart_id 
    order_obj=None ->initializing as None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")  ->Noting is their in the cart thats why rendering the page home
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)  ->creating or geeting the cart with the cart id
    return render(request, "carts/checkout.html", {"object": order_obj}) ->sending the order_id to the checkout.html

-----------------------------------------------------------------------------
Checkout.html
-----------------------------------------------------------------------------
{% extends "base.html" %}
{% block content %}
<h1>Checkout</h1>
<p>Cart total: {{ object.cart.total }}</p>   ->Showing the cart total as the object is came to this page
<p>Shipping Total total: {{ object.shipping_total }}</p>  ->Showing the shippig total
<p>Order Total: {{ object.total }}</p>   ->Showing the object total
{% endblock %}



------------------------------------------------------------------------------
Creating the accounts app
------------------------------------------------------------------------------
!!)python manage.py startapp accounts

**))views.py  ->accounts

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url   ->if the user is going through the url
# Create your views here.
def login_page(request):
    form = LoginForm(request.POST or None)
    context ={
        "form": form
    }
    #print(request.user.is_authenticated())
    next_ = request.GET.get('next')  ->geting the value what is entered in the url
    next_post = request.POST.get('next')   ->geting the url what is posted in that url
    redirect_path = next_ or next_post or None  ->is their is something that it goes to the variable
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        #print(int(request.user.is_authenticated()))
        if user is not None:
            #print(request.user.is_authenticated())
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("error")
            # Return an 'invalid login' error message.
    return render(request, "accounts/login.html", context)
user = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context={
        "form":form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = user.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "accounts/register.html", context)


Forms.py ->created in the accounts

##)forms.py

from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField( widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField( widget =forms.EmailInput)
    password = forms.CharField( widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username taken")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email taken")
        return email

^^)added te accounts to the setting.py of the ecommerce

-----------------------------------------------------------------------------
For the logout
-----------------------------------------------------------------------------
@@)urls.py   ->ecommerce

from django.contrib.auth.views import LogoutView  ->pre defined class

url(r'^logout/$', LogoutView.as_view(), name='logout'),

@@)setting.py ->ecommerce

   LOGOUT_REDIRECT_URL = '/login/'

@@)Navbar.html
	{% url 'logout' as logout%}

<li class="nav-item {% if request.path == login %} active {% endif %}">
          <a class="nav-link " href="{{ logout }}">logout</a>
</li>


-----------------------------------------------------------------------------
For Billing
-----------------------------------------------------------------------------
##)python manage.py startapp billing


##)Models.py

from django.db import models
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  ->so that for one user their will be only one billing profile
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email
def user_created_receiver(sender, instance,  created, *args, **kwargs):
    if created and instance.email:  ->if email is having the value than create the billing profile
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
post_save.connect(user_created_receiver, sender=User)


-----------------------------------------------------------------------------
Adding the billing profile with the cart
-----------------------------------------------------------------------------
@@@@)view.py ->cart.html

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    user = request.user   ->getting the user
    billing_profile = None  ->assing the billing_profile as the none
    login_form = LoginForm() ->calling the function from the accounts.forms
    if user.is_authenticated: ->if the user is authenticated than the sendingthe user and the email to the get the billing profile or create the user
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form
    }
    return render(request, "carts/checkout.html", context)

@@@)form.html->creating the file in account->snippets->form.html

<form method='POST' action='{%url "login" %}'>{% csrf_token %}
  {% if next %}
    <input type='hidden' name='next' value='{{next_url}}' />
  {% endif %}
{{ form }}
<button type="submit" class="btn btn-danger">Submit</button>
</form>

@@)checkout.html

{% extends "base.html" %}
{% block content %}
{% if not billing_profile %} ->if billing profile cntains the nothing
<viv class="row">
  <div class="col-12 col-md-6">
    <p class="lead">Login</p>
    {% include 'accounts/snippets/form.html' with form=login_form %} ->calling the form.html of the account snippets
  </div>
  <div class="col-12 col-md-6">
      <p class="lead">Continue as a guest</p>
  </div>
</div>

-----------------------------------------------------------------------------
FOR GUEST LOGIN
-----------------------------------------------------------------------------

##)forms.py --account

class GuestForm(forms.Form): ->taking email as the input field
    email = forms.EmailField()
##)view.py ---accounts

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context ={
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email") ->getting it from the form
        new_guest_email  = GuestEmail.objects.create(email=email) ->saving the form in the database a
        request.session['guest_email_id'] = new_guest_email.id create the seeson for the id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")

###Models.py  --account.py

from django.db import models
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#### admin.py  -----account.py

from django.contrib import admin

# Register your models here.
from .models import GuestEmail

admin.site.register(GuestEmail)


#####Urls.py  ---ecommere

from accounts.views import login_page, register_page, guest_register_view
url(r'^register/guest/$', guest_register_view, name='guest_register'),


####View.py   ----cart

from accounts.models import GuestEmail
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form
    }
    return render(request, "carts/checkout.html", context)


####checkout.html

<div class="col-12 col-md-6">
    <p> Continue as the guest </p>
    {% url "guest_register" as guest_register_url %}
    {% include 'accounts/snippets/form.html' with form=guest_form next_url=request.build_absolute_uri action_url=guest_register_url%}
  </div>

-----------------------------------------------------------------------------
When guest user want to login in between 
-----------------------------------------------------------------------------
###)Models.py ---- Order

from billing.models import BillingProfile
billing_profile= models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)

###)view.py ---------accounts.py

if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        #print(int(request.user.is_authenticated()))
        if user is not None:
            #print(request.user.is_authenticated())
            login(request, user)
            try:
                del request.session['guest_email_id']   ->when logged than delete the session with session
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("error")
            # Return an 'invalid login' error message.
    return render(request, "accounts/login.html", context)

######)view.py   ----carts

checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass
    if billing_profile is  not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj, active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

-----------------------------------------------------------------------------
defining the function inside the model
-----------------------------------------------------------------------------
view.py  ->cart

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    login_form = LoginForm()
    guest_form = GuestForm()
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)  ->calling the object of the billing new_or_get
    if billing_profile is  not None:
        order_obj, order_obj_created= Order.objects.new_or_get(billing_profile, cart_obj)
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form
    }
    return render(request, "carts/checkout.html", context)


######)Models.py --Billing

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, created

objects = BillingProfileManager()

###)Models.py   ->cart

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if  qs.count() == 1:
            new_obj=False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

-----------------------------------------------------------------------------
Making the addrress App 
-----------------------------------------------------------------------------
python mange.py startapp addrresses

models.py  ->addresses

from django.db import models
from billing.models import BillingProfile
# Create your models here.
ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    Address_type =    models.CharField(max_length=120, choices=ADDRESS_TYPE)
    Address_line_1 = models.CharField(max_length=120)
    Address_line_1 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='India')
    state = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)



####admin.py  - >address

from django.contrib import admin

# Register your models here.
from .models import Address

admin.site.register(Address)

########form.py
from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address


######)view.py ----cart

from addresses.forms import AddressForm

address_form = AddressForm()
billing_address_form = AddressForm()


    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": "address_form",
        "billing_address_form": "billing_address_form"
    }






-----------------------------------------------------------------------------
Ajax call
-----------------------------------------------------------------------------


*)Update-cart.html

<form class="form-product-ajax" method="POST" action='{% url "cart:update" %}' class="form"/> {% csrf_token %} @@@@class we defined is for ajax call

  <input type="hidden" name="product_id" value="{{ product.id }}" />
  {% if lists %}
    In cart<button type="submit" class="btn btn-link">Remove?</button>
  {% else %}
    {% if product in cart.products.all %}
      In cart<button type="submit" class="btn btn-link">Remove</button>
    {% else %}
      In cart<button type="submit" class="btn btn-success">Add to cart</button>
    {% endif %}
  {% endif %}
</form>


*)base.html
<script>
      $(document).ready(function(){
        var productForm = $(".form-product-ajax") selected the class from the form
        productForm.submit(function(event){
          event.preventDefault();   ->prevented the default reloading
          console.log("form is not sending")
          var thisForm = $(this)  ->so that the attribute can be accessed
          var actionEndpoint=  thisForm.attr("action"); ->taken the url
          var httpmethod= thisForm.attr("method");  ->taken the method
          var formData = thisForm.serialize();

          $.ajax({
            url: actionEndpoint,
            method: httpmethod,
            data:  formData,
            Success: function(data){
              console.log("Success")
              console.log(data)
            },
            error: function(data){
              console.log("error")
              console.log(errorData)
            }
          })

        })
      })
    </script>

-----------------------------------------------------------------------------
Ajax call for adding 
-----------------------------------------------------------------------------	


*)view.py cart

if product_id is not None:
        try:
            product_obj = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False  ->If removed than the added is turned into false
        else:
            cart_obj.products.add(product_obj)
            added = True   ->If the product is added than the added is true
        request.session['cart_items'] = cart_obj.products.count()
    if request.is_ajax(): ->request is from the ajax base.html
        print("Ajax request")
        json_data= { creating the json dictionary
            "added": added,  ->sending the added
            "removed": not added,
        }
        return JsonResponse(json_data) ->sending the response
    return redirect("cart:home")

**)Update-cart.html

<form class="form-product-ajax" method="POST" action='{% url "cart:update" %}' class="form"/> {% csrf_token %}
  <input type="hidden" name="product_id" value="{{ product.id }}" />
  {% if lists %}
    In cart<button type="submit" class="btn btn-link">Remove?</button>
  {% else %}
    <span class='submit-span'> ->defining the span class
    {% if product in cart.products.all %}
      In cart<button type="submit" class="btn btn-link">Remove</button>
    {% else %}
      <button type="submit" class="btn btn-success">Add to cart</button>
    {% endif %}
    </span>
  {% endif %}
</form>


@@@@@base.html

<script>
      $(document).ready(function(){
        var productForm = $(".form-product-ajax")
        productForm.submit(function(event){
          event.preventDefault();
          console.log("form is not sending")
          var thisForm = $(this)
          var actionEndpoint=  thisForm.attr("action");
          var httpMethod= thisForm.attr("method");
          var formData = thisForm.serialize();

          $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){  ->getting the dictionary from the ajax
              var submitSpan = thisForm.find(".submit-span") ->update cart 		class
              if (data.added){  ->if the item is added
                submitSpan.html("In cart <button type='submit' class='btn 		btn-link'>Remove?</button>")
              }
              else {
                submitSpan.html("<button type='submit'  class='btn btn-success'>Add to cart</button>")
              }
            },
            error: function(errordata){
              console.log("error")
              console.log(errorData)
            }
          })

        })
      })
    </script>

-----------------------------------------------------------------------------Updating the Cart ajax
-----------------------------------------------------------------------------
@@@ navbar.html    

  <li class="nav-item {% if request.path == cart_url %} active {% endif %}">
        <a class="nav-link " href="{{ cart_url }}"><span class="navbar-cart-count">{{ request.session.cart_items }}</span> <i class="fas fa-shopping-cart"></i></a>
      </li>

----->>>>>>>>>>>>>span is written to access the navabar cart

@@@@@@@@Navbar.html

"cartItemCount": cart_obj.products.count()  ->Getting the count from the database.

@@@@@@@@@base.html

var navbarCount =$(".navbar-cart-count") ->Selecting the Navbar
navbarCount.text(data.cartItemCount)  ->Changing the text with the cartItemCount sent from the view.py


-----------------------------------------------------------------------------
Refreshing the Cart when the value isremoved from the cart 
-----------------------------------------------------------------------------
ajax contain the three data basically the 

1)url :-where it is going from the form 

2)method:- what type of the method is this like post or the get data  

3)data:-what the form is containing

@@@)update-cart.html

<form class="form-product-ajax" method="POST" action='{% url "cart:update" %}' data-endpoint='{% url "cart:update" %}' class="form"/> {% csrf_token %}

###data-endpoint contain the next url link

@@@@)base.html

  var currentPath = window.location.href  -> take the current location postition
              if(currentPath.indexOf("cart") != -1)  ->if the current location is cart
              {
                refreshCart() ->call the function 
              }

@@@@@@cart ->template ->home.html

<table class="table cart-table">
   -> the class is defined so that we can use in the ajax 
<thead>
  
  <tr>
      
<th scope="row"></th>
      
<td>Product Name</td>
      
<td>Product Price</td>
    
</tr>
  </thead>
  
<tbody class="cart-body">   ->the class is defined so that we can use in the ajax 


@@@@@@base.html


function refreshCart(){   ->as the current position is cart than this function is called
          var cartTable = $(".cart-table") ->the cart-table is selected
          var cartBody = cartTable.find(".cart-body")  -> the cart-body is found
          cartBody.html("<h1>Changed</h1>") -> the html is changed


function refreshCart(){
          console.log("in current cart")
          var cartTable = $(".cart-table")
          var cartBody = cartTable.find(".cart-body")
          cartBody.html("<h1>Changed</h1>")
          var refreshCartUrl = '/api/cart'
          var refreshCartMethod = "GET";
          var data = {};
          $.ajax({
            url:refreshCartUrl,
            method:refreshCartMethod,
            data:data,
            sucess: function(data){
              console.log("Success")
            },
            error : function(errorData){
              console.log("error")
              console.log(errorData)
            }
          })
        }

@@@@@views.py carts

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{"name": x.name, "price":x.price} for x in cart_obj.products.all()]
    data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(data) ->send the response when it is called


@@@@@urls.py ecommerce

from carts.views import cart_detail_api_view
url(r'^api/cart$', cart_detail_api_view, name='api-cart'),


@@@@@carts->template->home.html

<tbody class="cart-body">
   
 <div class="cart-products">
    ->class is defined as we can use in ajax
  {% for product in cart.products.all %}
   
 <tr>
     
 <th scope="row">{{forloop.counter}}</th>
   
   <td>
<a href="{{ product.get_absolute_url }}">{{ product.title }}</a>
  
      {% include 'products/snippets/update-cart.html' with list=True product=product cart=cart %}
   
   </td>
     
 <td>
{{ product.price }}
</td>
    
</tr>
    
{% endfor %}
    
</div>
   
 <tr>
      
<td colspan="2"></td>
      
<td><b>Subtotal</b><span class="cart-subtotal">{{ cart.subtotal}}</span></td>
    </tr>
  ->class is defined so that we can chnage the value
  <tr>
     
 <td colspan="2"></td>
     
 <td><b>Total</b><span class="cart-total">{{ cart.total}}</span></td>
->->class is defined so that we can chnage the value


@@@@@@@Base.html

var refreshCartUrl = '/api/cart' ->call the cart_detail_api_view
          var refreshCartMethod = "GET";
          var data = {};
          $.ajax({
            url:refreshCartUrl,
            method:refreshCartMethod,
            data:data,
            success: function(data){
              console.log(data)
              if(data.products.length > 0)
              {
                productRows.html("<tr><td colspan=3>Coming Soon</td></tr>")
                cartBody.find("cart-subtotal").text(data.subtotal)
                cartBody.find("cart-total").text(data.subtotal)
              }
              else{
                window.location.href = currentUrl  ->refresh the page 
              }
            },
            error : function(errorData){
              console.log("error")
              console.log(errorData)
            }
          })
        }
      })














































































































































































 
























































































































