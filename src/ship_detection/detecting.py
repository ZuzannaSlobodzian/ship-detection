import ee
from .layout import *
from .masks import *

def ships(date, region):
    mosaic_image_sent1, vis_params_sent1 = sentinel1(date, region)
    radar_mosaic_sea = mosaic_image_sent1.updateMask(water_mask(region))

    ships = radar_mosaic_sea.select('VV').gt(2)
    return ships.updateMask(ships.neq(0))

def canny_edge_detector(date, region):
    background_layer = ee.Image.constant(0).clip(region)
    dilated_ships_layer = dilate(ships(date, region), 500)

    mask = dilated_ships_layer.eq(1)    
    combined_layer = background_layer.where(mask, 1)
    
    edges = ee.Algorithms.CannyEdgeDetector(combined_layer, threshold=0.1, sigma=1)
    return edges.updateMask(edges)