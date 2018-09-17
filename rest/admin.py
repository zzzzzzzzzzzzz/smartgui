from django.contrib import admin


# Register your models here.
from rest.models import Sensor, Measure

admin.site.register(Sensor)
admin.site.register(Measure)
