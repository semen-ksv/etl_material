from django.db import models

from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class MaterialData(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    uuid = models.IntegerField(unique=True, db_index=True)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    material_type = models.IntegerField()
    amount = models.IntegerField(null=True, blank=True)
    license = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    cultivation_tax = models.IntegerField(null=True, blank=True)
    amount_history = models.JSONField(null=True, blank=True)
    slug = models.CharField(max_length=15)
    sequence = models.IntegerField()
    creation_run = models.IntegerField(null=True, blank=True)
    strain = models.IntegerField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, null=True, blank=True)
    custom_fields = models.JSONField(null=True, blank=True)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    kind = models.CharField(max_length=30, null=True, blank=True)


class StatisticMaterialType(models.Model):

    material_type = models.IntegerField(unique=True, db_index=True)
    material_name = models.CharField(max_length=30, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)


class StatisticMaterialMeasureUnit(models.Model):

    short_name = models.CharField(max_length=10, null=True, blank=True)
    measure_type = models.CharField(max_length=30, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
