from django.db import models
from django.utils import timezone


class sku_modal(models.Model):
    country = models.CharField(max_length=100)
    dali_ref = models.CharField(max_length=100)
    sku_id = models.CharField(max_length=100)
    sku_url = models.CharField(max_length=255)
    catalog = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    percent = models.CharField(max_length=100)
    min_price = models.CharField(max_length=100)
    max_price = models.CharField(max_length=100)
    unit_cost = models.CharField(max_length=100)
    note = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.country


class sku_setting(models.Model):
    timer = models.CharField(max_length=20)
    uae_box = models.CharField(max_length=100)
    uae_box_price = models.CharField(max_length=100)
    ksa_box = models.CharField(max_length=100)
    ksa_box_price = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
