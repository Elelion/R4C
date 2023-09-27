

from django.db import models
from django.utils import timezone

from customers.models import Customer
from robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    quantity = models.PositiveIntegerField(default=0)  # Установите значение по умолчанию
    order_date = models.DateTimeField(default=timezone.now)
