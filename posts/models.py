from django.db import models

from authentication.models import Driver
from core.models import City
from project import settings


class Post(models.Model):
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    to_address_line = models.TextField(null=True)
    to_city = models.ForeignKey(
        City,
        models.RESTRICT,
        related_name='pickup_posts',
        null=True,
    )
    from_address_line = models.TextField(null=True)
    from_city = models.ForeignKey(
        City,
        models.RESTRICT,
        related_name='delivery_posts',
        null=True,
    )
    pickup_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    max_weight = models.FloatField()
    max_size = models.FloatField()
    delivery_fee = models.FloatField(null=True)
    delivery_commission = models.FloatField(null=True)
    created_by = models.ForeignKey(
        Driver,
        models.CASCADE,
        related_name='driver_posts',
        null=True
    )

    def __str__(self):
        return self.description



