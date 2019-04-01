from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import ContactForm
from django.contrib.auth import authenticate, login, get_user_model
def home_page(request):
    context = {
        "content": "Welcome to the homepage",
        "title":"hello shubham welcome to the home page"
    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAAAHHHHH"
    return render(request, "home_page.html", context)
def about_page(request):
    return render(request, "about_page.html", {})
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"hello shubham welcome to the contact page",
        "form": contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    #if request.method == "POST":
    #    print(request.POST)
    #    print(request.POST.get('fullname'))
    return render(request, "contact/view.html", context)
def home_page_old(request):
    return HttpResponse("<h1>hello world</h1>")
