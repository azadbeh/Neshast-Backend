from rest_framework import serializers

from apps.organizations.models import Organization
from apps.organizations.serializer import OrganizationSerializer

from ..models import Event, EventCategory, TicketType
from .ticket import TicketTypeSerializer


class EventSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    ticket_types = TicketTypeSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            "public_id",
            "title",
            "description",
            "organization",
            "ticket_types",
            "image",
            "category",
            "start_date",
            "end_date",
            "location",
            "max_participants",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]


class EventCreateSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True)
    organization = serializers.SlugRelatedField(slug_field="public_id", queryset=Organization.objects.all())
    category = serializers.SlugRelatedField(slug_field="public_id", queryset=EventCategory.objects.all())

    def create(self, validated_data):
        ticket_types_data = validated_data.pop("ticket_types")
        event = Event.objects.create(**validated_data)
        for ticket_type_data in ticket_types_data:
            TicketType.objects.create(event=event, **ticket_type_data)
        return event

    class Meta:
        model = Event
        fields = [
            "public_id",
            "title",
            "description",
            "organization",
            "image",
            "category",
            "start_date",
            "end_date",
            "location",
            "ticket_types",
        ]
        read_only_fields = ["public_id"]
