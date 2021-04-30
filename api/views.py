
from django.shortcuts import render, get_object_or_404

from api.models import StatisticMaterialMeasureUnit, StatisticMaterialType, MaterialData
from api.services import denormilize_data


def index(request):
    data = 'trooo'
    return render(request, 'index.html', {'page_obj': data})


def denorvilization(request):
    denormilize_data()
    table_data = MaterialData.objects.all()
    return render(request, 'denormilize_table.html', {'page_obj': table_data})


def build_graphs(request):

    measure_init_data =[]
    measure_init = StatisticMaterialMeasureUnit.objects.all()
    for item in measure_init:
        measure_init_data.append((item.measure_type, item.amount, item.cost))

    material_type_data=[]
    material_type = StatisticMaterialType.objects.all()
    for item in material_type:
        material_type_data.append((item.material_name, item.amount, item.cost))

    data = {'measure_init': measure_init_data,
            'material_type': material_type_data,
            'measure_data': measure_init,
            'material_type_data': material_type}
    return render(request, 'graph_dashboard.html', data)

