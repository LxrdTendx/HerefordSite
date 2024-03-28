from django.db import models
import os
from django.utils.timezone import now
from django.urls import reverse
class Region(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Регион')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/', verbose_name='Изображение')
    caption = models.TextField(blank=True, null=True, verbose_name='Подпись')

    def __str__(self):
        return f"Карусель изображений {self.id}"

    class Meta:
        verbose_name = 'Изображение для карусели'
        verbose_name_plural = 'Изображения для карусели'

class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Тип продукта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'

class SubProductType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Подтип продукта')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name='Тип продукта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подтип продукта'
        verbose_name_plural = 'Подтипы продуктов'

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name='Тип продукта')
    sub_product_type = models.ForeignKey(SubProductType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Подтип продукта')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Регион')
    farm = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ферма')
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Контактный телефон')
    details = models.TextField(blank=True, null=True, verbose_name='Детали')
    product_photo = models.ImageField(upload_to='products_photos/', blank=True, null=True, verbose_name='Фото продукта')
    age = models.CharField(max_length=255, blank=True, null=True, verbose_name='Возраст')
    price = models.CharField(max_length=255, blank=True, null=True, verbose_name='Цена')

    def __str__(self):
        return f"{self.product_type.name} - {self.sub_product_type.name if self.sub_product_type else ''}"

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Farm_point(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    contact_phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Регион')
    website = models.CharField(max_length=50, null=True, verbose_name='Веб-сайт')
    pdf_page = models.IntegerField(null=True, blank=True, verbose_name='Начальная страница PDF')  # обновлено
    pdf_page_end = models.IntegerField(null=True, blank=True, verbose_name='Конечная страница PDF')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фермерская точка'
        verbose_name_plural = 'Фермерские точки'

def news_image_path(instance, filename):
    # Форматируем дату в нужный формат, например '07-02-2024'
    # Если у новости уже есть дата, используем ее, иначе используем текущую дату
    date_str = instance.date.strftime('%d-%m-%Y') if instance.date else now().strftime('%d-%m-%Y')
    # Собираем путь, используя сформированную строку даты
    return os.path.join('news', date_str, filename)

class News_Page(models.Model):
    title = models.CharField(max_length=70, unique=True, verbose_name='Заголовок')
    text = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Текст')
    date = models.DateField(verbose_name='Дата')
    photo1 = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Фото 1')
    photo2 = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Фото 2')
    photo3 = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Фото 3')
    photo4 = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Фото 4')
    photo5 = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Фото 5')
    photo6 = models.ImageField(upload_to=news_image_path, blank=True, null=True, verbose_name='Фото 6')

    def get_photos(self):
        photos = [self.photo1, self.photo2, self.photo3, self.photo4, self.photo5, self.photo6]
        return [photo.url for photo in photos if photo]

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Страница новостей'
        verbose_name_plural = 'Новости'




class DishRecipe(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name='Название стейка')
    recipe = models.TextField(max_length=6000, blank=True, null=True, verbose_name='Рецепт')
    photo = models.ImageField(upload_to="recipes/", blank=True, null=True, verbose_name='Фото')

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    def get_photos(self):
        photos = [self.photo]
        return [photo.url for photo in photos if photo]

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'