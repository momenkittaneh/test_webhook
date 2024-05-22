from rest_framework import serializers


class TicketReplySerializer(serializers.Serializer):
    id = serializers.CharField()
    description = serializers.CharField(required=False)


class TicketSerializer(serializers.Serializer):
    description = serializers.CharField()
    username = serializers.CharField()
    comments = TicketReplySerializer(many=True)
    via_channel = serializers.CharField(required=False)
    via_source = serializers.CharField(required=False)
