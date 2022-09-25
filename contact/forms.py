from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    A class for contact form
    """
    class Meta:
        model = Contact
        fields = '__all__'
