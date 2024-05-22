from . import serializers, models
from django.conf import settings
from rest_framework import generics, response, status
import datetime
from django.contrib.auth.models import User
from django.views import generic as views_generic


class ZenDeskWebHookApiView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        serialized_data = serializers.TicketSerializer(data=data.get('ticket'))
        ticket_subject = models.TicketSubject.objects.filter(name=settings.ZENDESK_TICKET_SUBJECT).first()
        zendesk_user = User.objects.get(username=settings.ZENDESK_USER)
        if serialized_data.is_valid(raise_exception=True):
            requested_data = serialized_data.data
            try:
                service = models.CustomerService.objects.get(username=requested_data.get('username'))
                service_ticket = models.Ticket()
                ticket_content = f"""
                <p>Via Channel: {requested_data.get('channel')}</p>
                <p>Via Source: {requested_data.get('source')}</p>
                <p>Subject: {requested_data.get('subject')}</p>
                <p>Content: {requested_data.get('description')}</p>
                """
                service_ticket.subject = ticket_subject
                service_ticket.type_id = ticket_subject.type_id
                service_ticket.status = models.TICKET_STATUS_CLOSED
                service_ticket.closed_on = datetime.datetime.now()
                service_ticket.closed_by = zendesk_user
                service_ticket.created_by = zendesk_user
                service_ticket.content = ticket_content
                service_ticket.customerservice = service
                service_ticket.customer_id = service.customer_id
                service_ticket.save()
                replies = requested_data.get('comments')
                for reply in replies:
                    ticket_reply = models.Ticketreply()
                    ticket_reply.ticket_id = service_ticket.id
                    ticket_reply.ticketreply = reply.get('description') or "empty"
                    ticket_reply.created_by = zendesk_user
                    ticket_reply.save()

                return response.Response('Ticket Has Been Added Successfully', status.HTTP_200_OK)
            except Exception as e:
                return response.Response('SomeThing Went Wrong', status.HTTP_400_BAD_REQUEST)
        return response.Response('SomeThing Went Wrong', status.HTTP_400_BAD_REQUEST)


class TicketList(views_generic.ListView):
    queryset = models.Ticket.objects.all()
    template_name = 'tickets.html'
    context_object_name = 'tickets'
