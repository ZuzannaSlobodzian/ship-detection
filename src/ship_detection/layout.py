import ee
import geemap.foliumap as geemap
from .regions import combine_regions


def sentinel1(date, region):
    collection = (
        ee.ImageCollection('COPERNICUS/S1_GRD')
        .filterBounds(region)
        .filterDate(date[0], date[1])
    )

    images = collection.limit(10)  
    clipped_images = images.map(lambda img: img.clip(region))
    mosaic_image = clipped_images.mosaic()
    vis_params = {'min': -25, 'max': 0}
    return [mosaic_image, vis_params]

def sentinel2(date, region): #TODO Remove this
    collection = (
        ee.ImageCollection('COPERNICUS/S2_SR')
        .filterDate(date[0], date[1])
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 15))
    )

    image = collection.median()
    image = image.clip(region)
    vis = {
        'min': 0.0,
        'max': 3000,
        'bands': ['B4', 'B3', 'B2'],
    }
    return [image, vis]

def prepare_map(date, region):
    map = geemap.Map(center=(30, 0), zoom=3)

    mosaic_image_sent1, vis_params_sent1 = sentinel1(date, region)
    map.addLayer(mosaic_image_sent1, vis_params_sent1, 'Sentinel-1')
    return map

def prepare_basemap():
    basemap = geemap.Map(center=(30, 0), zoom=3)
    combined_geom = combine_regions()
    layer = ee.FeatureCollection(ee.Feature(combined_geom)).style(**{
        'color': '0000FF',  
        'width': 2,
    }).set('fillColor', '0000FF').set('fillOpacity', 0.4)

    basemap.addLayer(layer, {}, "Regions")
    return basemap

