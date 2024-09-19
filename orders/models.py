from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import Client
from posts.models import Post


# Create your models here.
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        CANCELED = 'canceled', _('Canceled')

    class PaymentStatus(models.TextChoices):
        PAID = 'paid', _('Paid')
        UNPAID = 'unpaid', _('Unpaid')

    post = models.ForeignKey(
        Post,
        models.RESTRICT,
        related_name='orders',
        null=True,
    )
    client = models.ForeignKey(
        Client,
        models.CASCADE,
        related_name='useer_orders',
        null=True
    )
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=16,
        choices=Status,
        default=Status.PENDING,
    )
    payment_status = models.CharField(
        max_length=16,
        choices=PaymentStatus,
        default=PaymentStatus.UNPAID,
    )
    client_notes = models.CharField(max_length=255)
    pickup_time = models.DateTimeField(null=True)
    arrival_time = models.DateTimeField(null=True)

    # pickup_address_line = models.CharField(max_length=255, null=True)
    # delivery_address_line = models.CharField(max_length=255, null=True)
