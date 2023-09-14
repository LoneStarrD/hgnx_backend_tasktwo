from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

