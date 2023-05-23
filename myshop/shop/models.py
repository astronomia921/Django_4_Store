from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(
                fields=['name']
            ),
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категории продуктов',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование продукта',
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    price = MoneyField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        default_currency='RUB'
    )
    available = models.BooleanField(
        verbose_name='Доступность товара',
        default=True,
    )
    created = models.DateTimeField(
        verbose_name='Дата создания позиции',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name='Дата обновления позиции',
        auto_now=True,
    )

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            args=[self.id, self.slug])
