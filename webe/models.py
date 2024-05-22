from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

TICKET_STATUS_CLOSED = 'Closed'


class Customer(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class CustomerService(models.Model):
    customer = models.ForeignKey(Customer, related_name='services', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class TicketType(models.Model):
    name = models.CharField(max_length=150)


class TicketSubject(models.Model):
    name = models.CharField(max_length=150)
    type = models.ForeignKey(TicketType, related_name='ticket_subjects', on_delete=models.PROTECT)


class Ticket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets', null=True)
    status = models.CharField(max_length=25)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    closed_on = models.DateTimeField(blank=True, null=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='closed_tickets', null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_tickets', null=True)
    content = RichTextField(blank=True, null=True, config_name='ticket-ckeditor')
    customerservice = models.ForeignKey(CustomerService, related_name='tickets', on_delete=models.PROTECT)
    type = models.ForeignKey(TicketType, related_name='tickets', on_delete=models.PROTECT)
    subject = models.ForeignKey(TicketSubject, related_name='tickets', on_delete=models.PROTECT)


class Ticketreply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    ticketreply = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
