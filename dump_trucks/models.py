from django.db import models
from django.contrib.gis.db import models as gis_models

class Truck(models.Model):
    board_number = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    max_capacity = models.PositiveIntegerField()
    current_weight = models.PositiveIntegerField()
    sio2_percent = models.FloatField()
    fe_percent = models.FloatField()

    def overload_percent(self):
        return max(0, round(((self.current_weight - self.max_capacity) * 100 / self.max_capacity), 2))

class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    current_weight = models.PositiveIntegerField()
    sio2_percent = models.FloatField()
    fe_percent = models.FloatField()
    polygon = gis_models.PolygonField()

class Unloading(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    in_poligon = models.BooleanField(default=False)

