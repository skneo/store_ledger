from django.db import models

# Create your models here.


class Inventory1(models.Model):
    id = models.AutoField(primary_key=True)
    inv_id = models.CharField(max_length=20)
    material_code = models.CharField(max_length=100)
    material_name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)
    remark = models.CharField(max_length=200)

    def __str__(self):
        return self.material_code


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    inv_id = models.CharField(max_length=20)
    material_code = models.CharField(max_length=100)
    material_name = models.CharField(max_length=200)
    in_out = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    # unit = models.CharField(max_length=20)
    issued_to = models.CharField(max_length=200)
    remark = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)
