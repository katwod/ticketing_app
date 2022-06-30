from django.urls import path
from . import views

urlpatterns = [
    path("login", views.Login, name ="login"),
    path("assistanteDZ", views.AssistanteDZ, name ="assistanteDZ"),
    path('assistanteDZ/ticket/<int:ticket_id>', views.ticket_by_id, name='dz_ticket_by_id'),
    path('assistanteDZ/markTicketComplete', views.openUploadForm, name='markTicketComplete'),
    path('assistanteDZ/ticketComplete/<int:ticket_id>', views.ticketComplete, name='ticketComplete'),
    path("assistanteDZ/assignTicket", views.AssignTicket, name ="assignTicket"),
    path('assistanteFR/ticket/<int:ticket_id>', views.ticket_by_id, name='fr_ticket_by_id'),
    path("assistanteFR", views.AssistanteFR, name ="assistanteFR"),
    path("assistanteFR/newTicket", views.openCreateForm, name ="openNewTicket"),
    path("assistanteFR/newTicketCreate", views.newTicketCreation, name ="newTicket"),
    path('assistanteFR/filterTickets', views.filterTickets, name='ticketFiltered'),
    path("", views.downloadFile, name ="downloadFile"),
]