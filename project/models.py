from django.db import models


class Government(models.Model):
    id = models.AutoField()
    name = models.CharField(max_length=100)
    cities = models.ManyToOneRel('project.models.City', 'cities')

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.AutoField()
    name = models.CharField(max_length=100)
    government = models.ForeignKey(
        Government,
        models.CASCADE,
        related_name='cities'
    )

    def __str__(self):
        return self.name
