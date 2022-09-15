from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Support_Tickets, Tickets_Messages
from .forms import UserProfileForm, SupportTicketForm, SupportMessageForm

from checkout.models import Order

@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

# Used to display all support queries
@login_required
def display_tickets(request):
    tickets = Support_Tickets.objects.all().order_by("-created_on")
    tickets_open = tickets.filter(status="0", user=request.user)
    ticket_messages = Tickets_Messages.objects.filter(ticket=tickets)
    context = {
        'tickets_open': tickets_open,
        'ticket_messages': ticket_messages
        }
    return render(request, 'profiles/support.html', context)


# Add support ticket
@login_required
def add_support_ticket(request):
    form = SupportTicketForm()
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            messages.success(request, f'Your query has been added')
            new_form.save()
            return redirect('open-support-tickets')
    context = {
        'form': form
        }
    return render(request, 'profiles/add_ticket.html', context)


# Used for toggling links from visible to not visible
@login_required
def toggle_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Support_Tickets, id=ticket_id)
    if request.user == ticket.user:
        if ticket.status == 0:
            ticket.status = 1
            ticket.save()
        else:
            ticket.status = 0
            ticket.save

        return redirect('open-support-tickets')
    else:
        messages.warning(request, 'You do not have access to this page')
        return redirect('home')


# Used for getting support ticket details
@login_required
def ticket_details(request, ticket_id):

    ticket = get_object_or_404(Support_Tickets, id=ticket_id)

    form = SupportMessageForm()
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if request.user == ticket.user:
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.ticket = Support_Tickets.objects.get(id=ticket_id)
                messages.success(request, f'Your message has been posted')
                new_form.save()
                return redirect('ticket-details', ticket.id)
        else:
            messages.warning(request, 'You do not have access to this page')
            return redirect('home')

    if request.user == ticket.user:
        ticket_messages = Tickets_Messages.objects.all().filter(ticket=ticket)
        context = {
            'ticket': ticket,
            'ticket_messages': ticket_messages,
            'form': form
            }
        return render(request, 'profiles/ticket_detail.html', context)
    else:
        messages.warning(request, 'You do not have access to this page')
        return redirect('home')