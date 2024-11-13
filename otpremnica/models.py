from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Supplier(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=300, blank=False, null=False)
    id_supplier = models.CharField(max_length=13, blank=False, null=False, unique=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=300, blank=False, null=False)
    id_company = models.CharField(max_length=13, blank=False, null=False, unique=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    book_number = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.id_company


class MeatType(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_meat_type():
        try:
            default_meat = MeatType.objects.get(name='SVINJE')
        except ObjectDoesNotExist:
            default_meat = None
        return default_meat


class DispatchNote(models.Model):
    objects = models.Manager()
    index = models.PositiveIntegerField()
    doc_number = models.CharField(max_length=20, blank=False, null=False, unique=False)
    doc_date = models.DateField(default=date.today)
    supplier = models.ForeignKey(Supplier, related_name='suppliers', null=False, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, related_name='company', null=False, on_delete=models.PROTECT)
    meat_type = models.ForeignKey(MeatType, related_name='meat_type', null=False, on_delete=models.PROTECT,
                                  default=MeatType.get_meat_type)
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    total_mass = models.PositiveIntegerField(blank=True, null=True)
    mass = models.PositiveIntegerField(blank=True, null=True)
    passports = models.TextField(blank=True, null=True)
    certificate_id = models.TextField(blank=True, null=True)
    certificate_number = models.CharField(max_length=250, blank=True, null=True)
    sys_doc_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='dispatch_notes', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('doc_number', 'company')
