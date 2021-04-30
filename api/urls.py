from django.urls import path

from api.views import index, denorvilization, build_graphs

app_name = 'api'



urlpatterns = [
    path('', index, name='index_view'),
    path('denormilize/', denorvilization, name='denormilize'),
    path('build_graphs/', build_graphs, name='build_graphs'),
]