from rest_framework import serializers


class TicketReplySerializer(serializers.Serializer):
    description = serializers.CharField()


class TicketSerializer(serializers.Serializer):
    description = serializers.CharField()
    username = serializers.CharField()
    comments = TicketReplySerializer(many=True)
    via_channel = serializers.CharField()
    via_source = serializers.CharField()
