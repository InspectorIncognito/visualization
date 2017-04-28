import os
from django.contrib.gis.utils import LayerMapping
from .models import ZonificationTransantiago

world_mapping =  {
    'id' : 'id',
    'area' : 'area',
    'zona' : 'zona',
    'com' : 'com',
    'comuna' : 'comuna',
    'cartodb_id' : 'cartodb_id',
    'created_at' : 'created_at',
    'updated_at' : 'updated_at',
    'comunidad_field' : 'comunidad_',
    'geom' : 'MULTIPOLYGON',
}

world_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '777shapes', 'zonificacion_eod2012.shp'),
)

def run(verbose=True):
    lm = LayerMapping(
        ZonificationTransantiago, world_shp, world_mapping,
        transform=False, encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)
