import ee
# from .regions import *

def landcover(region):
    landcover = ee.ImageCollection('ESA/WorldCover/v200')
    return landcover.map(lambda image: image.clip(region))

def land_mask(region):
    first_image = landcover(region).first()
    land_mask = first_image.select('Map').neq(80)
    land_layer = first_image.updateMask(land_mask)
    return dilate(land_layer, 100) 

def water_mask(region):
    land_binary = land_mask(region).gt(0)
    land_binary = land_binary.unmask(0)
    return land_binary.Not()

def dilate(image, radius):
    dilated = image.focal_max(radius, 'circle', 'meters')
    return dilated
