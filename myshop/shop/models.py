from django.db import models
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            verbose_name='Название',
            max_length=200,
        ),
        slug=models.SlugField(
            verbose_name='Идентификатор',
            max_length=200,
            unique=True
        )
    )

    class Meta:
        # ordering = ('name',)
        # indexes = [
        #     models.Index(
        #         fields=['name']
        #     ),
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            max_length=200,
            verbose_name='Наименование продукта',
        ),
        slug=models.SlugField(
            verbose_name='Идентификатор',
            max_length=200,
        ),
        description=models.TextField(
            verbose_name='Описание',
            blank=True,
        )
        )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категории продуктов',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Цена',
        null=True,
        max_digits=10,
        decimal_places=2,
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
        # ordering = ('name',)
        indexes = [
            # models.Index(fields=['id', 'slug']),
            # models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            args=[self.id, self.slug])
