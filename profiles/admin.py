from django.contrib import admin
from .models import Support_Tickets, Tickets_Messages


@admin.register(Support_Tickets)
class TicketsAdmin(admin.ModelAdmin):
    # Support query admin
    list_display = ['user', 'title']
    search_fields = ['user__username', 'title']
    list_filter = ('user', 'status')


# Support Tickets MessagesAdmin
@admin.register(Tickets_Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'message']
    search_fields = ['user__username', 'ticket']
    list_filter = ('user',)
