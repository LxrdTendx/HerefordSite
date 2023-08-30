from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class SubProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    sub_product_type = models.ForeignKey(SubProductType, on_delete=models.CASCADE, null=True, blank=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    farm = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    product_photo = models.ImageField(upload_to='products_photos/', blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product_type.name} - {self.sub_product_type.name if self.sub_product_type else ''}"
