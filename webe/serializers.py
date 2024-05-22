from rest_framework import serializers


class TicketReplySerializer(serializers.Serializer):
    id = serializers.CharField()
    description = serializers.CharField(required=False)


class TicketSerializer(serializers.Serializer):
    description = serializers.CharField()
    username = serializers.CharField()
    comments = TicketReplySerializer(many=True)
    via = serializers.CharField(required=False)
