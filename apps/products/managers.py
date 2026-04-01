from django.db import models

class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=True, quantity__gt=0)