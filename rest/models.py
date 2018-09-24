# coding=utf-8
from django.db import models

# Create your models here.


class Sensor(models.Model):

    class Meta:
        verbose_name = u"Сенсор"
        verbose_name_plural = u"Сенсоры"

    name = models.CharField(
        verbose_name=u"Имя сенсора",
        blank=False,
        null=False,
        max_length=255,
        unique=True,
    )

    description = models.TextField(
        verbose_name=u"Описание отображаемой информации",
        blank=False,
        null=False,
    )


class Measure(models.Model):

    class Meta:
        ordering = ["timestamp"]
        verbose_name = "Значение сенсора"
        verbose_name_plural = "Значение сенсора"

    def __str__(self):
        return "{0.sensor.name} | {0.value}".format(self)

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.SET_NULL,
        default=1,
        related_name='sensor',
        null=True,
        blank=True,
        verbose_name="Сенсор/Счётчик/Датчик",
        help_text="Источник информации",
    )

    value = models.FloatField(
        default=0.0,
        null=False,
        blank=False,
        verbose_name=u"Значение"
    )

    timestamp = models.DateTimeField(
        verbose_name="Время",
    )
