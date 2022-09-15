from django.shortcuts import render
from .forms import ContactForm
# Create your views here.



def contact_us(request):
    """
    To get contact details from user
    """
    contact_form = ContactForm()
    contacted = False
    if request.method == 'GET':
        if not request.user.is_authenticated:
            contact_form = ContactForm()
        elif request.user.userprofile:
            contact_form = ContactForm(
                initial={
                    'email': request.user.email,
                    'phone': request.user.userprofile.default_phone_number,
                            }
                )
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            contacted = True
    context = {'contact_form': contact_form,
               'contacted': contacted, }

    return render(request, 'contact/contact.html', context)