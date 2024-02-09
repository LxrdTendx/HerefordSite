from django.db import models
import os
from django.utils.timezone import now
from django.urls import reverse
class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Carousel Image {self.id}"

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
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    farm = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    product_photo = models.ImageField(upload_to='products_photos/', blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product_type.name} - {self.sub_product_type.name if self.sub_product_type else ''}"


class Farm_point(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_phone = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.CharField(max_length=50, null=True)
    pdf_page = models.IntegerField(null=True, blank=True)  # новое поле для номера страницы PDF

    def __str__(self):
        return self.name


def news_image_path(instance, filename):
    # Форматируем дату в нужный формат, например '07-02-2024'
    # Если у новости уже есть дата, используем ее, иначе используем текущую дату
    date_str = instance.date.strftime('%d-%m-%Y') if instance.date else now().strftime('%d-%m-%Y')
    # Собираем путь, используя сформированную строку даты
    return os.path.join('news', date_str, filename)

class News_Page(models.Model):
    title = models.CharField(max_length=70, unique=True)
    text = models.TextField(max_length=6000, blank=True, null=True)
    date = models.DateField()
    photo1 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    photo2 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    photo3 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    photo4 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    photo5 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    photo6 = models.ImageField(upload_to=news_image_path, blank=True, null=True)

    def get_photos(self):
        photos = [self.photo1, self.photo2, self.photo3, self.photo4, self.photo5, self.photo6]
        return [photo.url for photo in photos if photo]

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])