from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    price = models.CharField(max_length=500, null=True, blank=True)
    shipfee = models.CharField(max_length=500, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.price


class Detail(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    sellerlink = models.CharField(max_length=500, null=True, blank=True)
    sellername = models.CharField(max_length=500, null=True, blank=True)
    itemlocation = models.CharField(max_length=500, null=True, blank=True)
    feedback = models.CharField(max_length=100, null=True, blank=True)
    sold = models.CharField(max_length=100, null=True, blank=True)
    

    def __str__(self):
        return self.sellername