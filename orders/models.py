from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import Client
from core.models import City
from posts.models import Post


# Create your models here.
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETED = 'completed', _('Completed')
        CANCELED = 'canceled', _('Canceled')
        REJECTED = 'rejected', _('Rejected')

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
    # Pickup details
    pickup_time = models.DateTimeField(null=True)
    # pickup_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='pickup_orders', null=False)
    pickup_address_line = models.CharField(max_length=255, null=True)

    # Arrival details
    arrival_time = models.DateTimeField(null=True)
    # arrival_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='delivery_orders', null=False)
    delivery_address_line = models.CharField(max_length=255, null=True)

    # Client notes
    client_notes = models.CharField(max_length=255)
    cargo_image = models.ImageField(upload_to='cargo_images', null=True, blank=True)

    # Payment
    paymob_order_id = models.CharField(max_length=255, null=True, default=None)

    # Order completed
    order_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"
