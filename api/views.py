
from django.shortcuts import render, get_object_or_404

from api.models import StatisticMaterialMeasureUnit, StatisticMaterialType, MaterialData
from api.services import denormalize_data


def index(request):
    """initial page with welcome text"""

    return render(request, 'index.html')


def denormalization(request):
    """run loading data from Storage and denormalize data"""
    denormalized_data = denormalize_data()
    if denormalized_data:
        table_data = MaterialData.objects.all()
        return render(request, 'denormalize_table.html', {'page_obj': table_data})
    else:
        return render(request, 'denormalize_table.html', {'msg': "Material data was empty or not loaded!"})


def build_graphs(request):
    """prepare data for graphs and table"""
    measure_init_data = []
    measure_init = StatisticMaterialMeasureUnit.objects.all()
    for item in measure_init:
        measure_init_data.append((item.measure_type, item.amount, item.cost))

    material_type_data = []
    material_type = StatisticMaterialType.objects.all()
    for item in material_type:
        material_type_data.append((item.material_name, item.amount, item.cost))

    data = {'measure_init': measure_init_data,
            'material_type': material_type_data,
            'measure_data': measure_init,
            'material_type_data': material_type}
    return render(request, 'graph_dashboard.html', data)

