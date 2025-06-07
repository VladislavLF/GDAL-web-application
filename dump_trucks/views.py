from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Truck, Unloading, Warehouse
from .forms import WarehouseForm
from django.contrib.gis.geos import Point
from .forms import TruckForm

def is_inside_storage(x, y, warehouse):
    point = Point(x, y)
    try:
        return warehouse.polygon.contains(point) or warehouse.polygon.touches(point)
    except Exception as e:
        print("Geometry error:", e)
        return False

def add_truck(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TruckForm()

    return render(request, 'dump_trucks/add_truck.html', {'form': form})

def calculate_storage(unloadings, warehouse):
    init_volume = warehouse.current_weight
    init_sio2 = warehouse.sio2_percent
    init_fe = warehouse.fe_percent
    final_volume = init_volume
    sio2_total = init_volume * init_sio2
    fe_total = init_volume * init_fe

    for unloading in unloadings:
        truck = unloading.truck
        if is_inside_storage(unloading.x, unloading.y, warehouse):
            final_volume += truck.current_weight
            sio2_total += truck.current_weight * truck.sio2_percent
            fe_total += truck.current_weight * truck.fe_percent

    if final_volume == 0:
        return 0, 0, 0

    return final_volume, round(sio2_total / final_volume, 2), round(fe_total / final_volume, 2)

def add_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = WarehouseForm()

    return render(request, 'dump_trucks/add_warehouse.html', {'form': form})

def index(request):
    trucks = Truck.objects.all()
    warehouses = Warehouse.objects.all()

    selected_warehouse_id = request.POST.get('warehouse') or request.GET.get('warehouse')
    selected_warehouse = Warehouse.objects.filter(id=selected_warehouse_id).first() if selected_warehouse_id else None

    if request.method == 'POST' and selected_warehouse:
        for truck in trucks:
            x = request.POST.get(f'x_{truck.id}')
            y = request.POST.get(f'y_{truck.id}')
            if x and y:
                x_val, y_val = float(x), float(y)
                inside = is_inside_storage(x_val, y_val, selected_warehouse)
                Unloading.objects.update_or_create(
                    truck=truck,
                    warehouse=selected_warehouse,
                    defaults={'x': x_val, 'y': y_val, 'in_poligon': inside}
                )
        url = reverse('index')
        return redirect(f'{url}?warehouse={selected_warehouse.id}')

    unloadings = Unloading.objects.filter(warehouse=selected_warehouse)

    if selected_warehouse:
        final_volume, final_sio2, final_fe = calculate_storage(unloadings, selected_warehouse)
    else:
        final_volume = final_sio2 = final_fe = None

    return render(request, 'dump_trucks/index.html', {
        'trucks': trucks,
        'unloadings': {u.truck.id: u for u in unloadings},
        'warehouses': warehouses,
        'selected_warehouse': selected_warehouse,
        'final_volume': final_volume,
        'final_sio2': final_sio2,
        'final_fe': final_fe,
    })
