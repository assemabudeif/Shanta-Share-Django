from django.db import models
from project.models import City


# Create your models here.
class Post(models.Model):
    id = models.AutoField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    to_address_line = models.TextField()
    to_city = models.ForeignKey(
        City,
        models.RESTRICT,
        related_name='posts'
    )
    from_address_line = models.TextField()
    from_city = models.ForeignKey(
        City,
        models.RESTRICT,
        related_name='posts'
    )
    pickup_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    max_weight = models.FloatField()
    max_size = models.FloatField()
    delivery_fee = models.FloatField()

    def __str__(self):
        return self.description
