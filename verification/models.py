from random import randbytes

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from verification.choices import VerificationTypeChoices

USER = get_user_model()


def generate_token():
    return randbytes(32).hex()


class VerificationToken(models.Model):
    """
    Model to store verification tokens for users
    """

    token = models.CharField(max_length=64, default=generate_token, editable=False)
    user = models.ForeignKey(to=USER, on_delete=models.CASCADE, related_name="verification_tokens")
    type = models.CharField(max_length=20, choices=VerificationTypeChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_for = models.DurationField()

    def __str__(self):
        return f"{self.user}'s {self.type} token"

    @property
    def is_expired(self):
        """
        Checks if the token is not expired
        """
        return self.created_at + self.valid_for < timezone.now()

    class Meta:
        ordering = ["-created_at"]
