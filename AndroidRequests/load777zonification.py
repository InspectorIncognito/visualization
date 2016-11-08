import os
from django.contrib.gis.utils import LayerMapping
from .models import zonificationTransantiago

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
        zonificationTransantiago, world_shp, world_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)