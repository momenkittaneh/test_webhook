from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Customer)
admin.site.register(models.CustomerService)
admin.site.register(models.TicketSubject)
admin.site.register(models.TicketType)
admin.site.register(models.Ticket)
