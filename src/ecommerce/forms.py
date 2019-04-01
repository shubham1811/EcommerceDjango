from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField( widget =forms.TextInput(attrs={"class": "form-control","placeholder":"your name"}))
    email = forms.EmailField( widget =forms.EmailInput(attrs={"class": "form-control","placeholder":"Your email"}))
    content = forms.CharField(widget =forms.Textarea(attrs={"class": "form-control","placeholder":"Your message"}))


    def clean_email(self):
        email= self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("email has to be gmail.com")
        return email
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        return data
