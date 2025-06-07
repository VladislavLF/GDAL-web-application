from .models import Unloading
from django import forms
from .models import Truck
from django.contrib.gis.geos import GEOSGeometry
from .models import Warehouse

class UnloadingForm(forms.ModelForm):
    class Meta:
        model = Unloading
        fields = ['truck', 'x', 'y']
        labels = {
            'truck': 'Самосвал',
            'x': 'Координата X',
            'y': 'Координата Y',
        }

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['board_number', 'model', 'max_capacity', 'current_weight', 'sio2_percent', 'fe_percent']
        labels = {
            'board_number': 'Бортовой номер',
            'model': 'Модель самосвала',
            'max_capacity': 'Макс. грузоподъемность (т)',
            'current_weight': 'Текущий вес (т)',
            'sio2_percent': 'Содержание SiO₂ (%)',
            'fe_percent': 'Содержание Fe (%)',
        }

class WarehouseForm(forms.ModelForm):
    area_wkt = forms.CharField(label='Полигон (WKT)')

    class Meta:
        model = Warehouse
        fields = ['name', 'current_weight', 'sio2_percent', 'fe_percent', 'area_wkt']
        labels = {
            'name': 'Название склада',
            'current_weight': 'Текущий вес (т)',
            'sio2_percent': 'Содержание SiO₂ (%)',
            'fe_percent': 'Содержание Fe (%)',
        }

    def clean_area_wkt(self):
        wkt_text = self.cleaned_data['area_wkt']
        try:
            geom = GEOSGeometry(wkt_text)
            if geom.geom_type != 'Polygon':
                raise forms.ValidationError("Геометрия должна быть полигоном.")
            return geom
        except Exception as e:
            raise forms.ValidationError(f"Ошибка при обработке WKT: {e}")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.polygon = self.cleaned_data['area_wkt']
        if commit:
            instance.save()
        return instance
