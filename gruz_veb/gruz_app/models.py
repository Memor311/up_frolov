from django.db import models
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

class TransportType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

class User(models.Model):
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес")
    role = models.ForeignKey(
        Role, 
        on_delete=models.PROTECT, 
        related_name='users',
        verbose_name="Роль"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def __str__(self):
        if self.patronymic:
            return f"{self.surname} {self.first_name} {self.patronymic}"
        return f"{self.surname} {self.first_name}"
    
class Cargo(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Вес")
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Объём")

    def __str__(self):
        return self.name

class Transport(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    transport_type = models.ForeignKey(
        TransportType, 
        on_delete=models.PROTECT, 
        related_name='transports',
        verbose_name="Тип транспорта"
    )
    transport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер транспорта")
    capacity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Вместимость")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.transport_number})"

class Route(models.Model):
    address_start = models.TextField(verbose_name="Адрес начала")
    address_end = models.TextField(verbose_name="Адрес конца")
    departure_date = models.DateTimeField(verbose_name="Дата отправления")
    driver = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='driver_routes',
        limit_choices_to={'role__name': 'Водитель'},
        verbose_name="Водитель"
    )
    client = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='client_routes',
        limit_choices_to={'role__name': 'Клиент'},
        verbose_name="Клиент"
    )
    transport = models.ForeignKey(
        Transport, 
        on_delete=models.PROTECT, 
        related_name='routes',
        verbose_name="Транспорт"
    )
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT, 
        related_name='routes',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

class Request(models.Model):
    cargo = models.ForeignKey(
        Cargo, 
        on_delete=models.CASCADE, 
        related_name='requests',
        verbose_name="Груз"
    )
    route = models.ForeignKey(
        Route, 
        on_delete=models.CASCADE, 
        related_name='requests',
        verbose_name="Маршрут"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")


class Tracking(models.Model):
    route = models.ForeignKey(
        Route, 
        on_delete=models.CASCADE, 
        related_name='trackings',
        verbose_name="Маршрут"
    )
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Время")
    action = models.TextField(verbose_name="Действие")