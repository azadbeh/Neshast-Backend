from enum import Enum

from django.conf import settings
from django.core import validators
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .event import Event


class TicketStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    @classmethod
    def choices(cls):
        return [(status.value, status.name.title()) for status in cls]


class TicketType(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField(validators=[validators.MinValueValidator(1)], null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="ticket_types")
    price = models.IntegerField(validators=[validators.MinValueValidator(0)])


class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(max_length=20, choices=TicketStatus.choices(), default=TicketStatus.PENDING.value)
    ticket_number = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        unique_together = ["user", "ticket_type"]

    def __str__(self):
        return f"Ticket {self.ticket_number} - {self.event.title}"

    def clean(self):
        """Validate ticket data"""
        if self.event.start_date < timezone.now():
            raise ValidationError("Cannot create ticket for past events")

        if self.event.max_participants:
            confirmed_tickets = (
                self.event.tickets.filter(status=TicketStatus.CONFIRMED.value).exclude(id=self.id).count()
            )
            if confirmed_tickets >= self.event.max_participants:
                raise ValidationError("Event has reached maximum participants")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def confirm(self):
        """Confirm the ticket"""
        if self.status == TicketStatus.PENDING.value:
            self.status = TicketStatus.CONFIRMED.value
            self.save()
            return True
        return False

    def cancel(self):
        """Cancel the ticket"""
        if self.status in [TicketStatus.PENDING.value, TicketStatus.CONFIRMED.value]:
            self.status = TicketStatus.CANCELLED.value
            self.save()
            return True
        return False

    def is_valid(self):
        """Check if ticket is valid"""
        if self.status != TicketStatus.CONFIRMED.value:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            self.status = TicketStatus.EXPIRED.value
            self.save()
            return False
        return True

    @classmethod
    def get_user_tickets(cls, user):
        """Get all tickets for a user"""
        return cls.objects.filter(user=user)

    @classmethod
    def get_event_tickets(cls, event):
        """Get all tickets for an event"""
        return cls.objects.filter(event=event)

    @property
    def event(self):
        return self.ticket_type.event
