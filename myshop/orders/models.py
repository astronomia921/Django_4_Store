from django.db import models
from django.conf import settings
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=250
    )
    postal_code = models.CharField(
        verbose_name='Почтовый индекс',
        max_length=20,
    )
    city = models.CharField(
        verbose_name='Город',
        max_length=100,
    )
    created = models.DateTimeField(
        verbose_name='Дата создания заказа',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='Дата обновления заказа',
        auto_now=True
    )
    paid = models.BooleanField(
        verbose_name='Статус заказа',
        default=False
    )
    stripe_id = models.CharField(
        verbose_name='Идентификатор платежа',
        max_length=250,
        blank=True
    )

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']), ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='order_items',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Колличество',
        default=1
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
