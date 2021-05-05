from django.urls import path

from api.views import index, denormalization, build_graphs

app_name = 'api'


urlpatterns = [
    path('', index, name='index_view'),
    path('denormalize/', denormalization, name='denormalize'),
    path('build_graphs/', build_graphs, name='build_graphs'),
]