import ee
import geemap.foliumap as geemap
from ship_detection import authenticate

credentials = authenticate.authorize()
ee.Initialize(credentials)
geemap.ee_initialize()

region_geoms = {
    "Gdańsk Bay": ee.Geometry.BBox(18.58, 54.69, 19.79, 54.34),
    "Black Sea": ee.Geometry.BBox(30.0, 46.0, 32.5, 45.0),
    "Caspian Sea": ee.Geometry.BBox(52.0, 41.0, 54.0, 40.0),
    "Red Sea": ee.Geometry.BBox(32.0, 30.0, 34, 27.4),
    "South China Sea / Philippines": ee.Geometry.BBox(119.0, 16.0, 120.0, 18.0),
    "Taiwan": ee.Geometry.BBox(120.0, 21.9, 121.6, 25.5),
    "Tokyo Bay": ee.Geometry.BBox(139.0, 34.4, 140.8, 35.7),
    "Panama Bay": ee.Geometry.BBox(-79.8, 8.1, -78.7, 9),
    "Lake Michigan (USA)": ee.Geometry.BBox(-87.5, 41.6, -86.4, 44),
    "Tatar Strait": ee.Geometry.BBox(139.0, 45.0, 141.3, 48.1),
    "Port Phillip": ee.Geometry.BBox(144.2, -38.6, 145.0, -37.8),
    "Tristan da Cunha": ee.Geometry.BBox(-12.8, -37.9, -11.9, -36.6),
    # "Iceland": ee.Geometry.BBox(-20, 63, -16.6, 64.0),
    "Palk Strait": ee.Geometry.BBox(79, 8.3, 80.1, 10.3),
    "Maldives": ee.Geometry.BBox(72.6, 2.9, 74.5, 7.1),
    "Bohai Sea": ee.Geometry.BBox(117.5, 37.1, 121.6, 40),
    "Port of Shanghai": ee.Geometry.BBox(121.7, 30.7, 122.6, 31.7),
    "Torres Strait": ee.Geometry.BBox(140, -11, 145, -9),
    "Gulf of Guinea": ee.Geometry.BBox(5.1, 1, 8, 4.4),
    "Azores": ee.Geometry.BBox(-28.9, 39.1, -24.9, 37.6),
    "Bahamas": ee.Geometry.BBox(-78.5, 23.5, -76, 25.5),
    "Strait of Dover": ee.Geometry.BBox(0.9, 50.9, 1.9, 51.1),
    "Kattegat": ee.Geometry.BBox(10.5, 56.8, 12, 57.9),
    "Los Angeles / Pacific Ocean": ee.Geometry.BBox(-119.4, 33.4, -118, 34),
    "Honolulu / Hawaii": ee.Geometry.BBox(-158.4, 21.1, -157.5, 21.8),
    # "Gulf of Ob": ee.Geometry.BBox(73.2, 67.5, 74.8, 68.5),
    "Bay of Bengal": ee.Geometry.BBox(91, 21.4, 92, 22.5),
    "Thane Creek": ee.Geometry.BBox(72.7, 18.8, 73, 19.05),
    "Rio de la Plata": ee.Geometry.BBox(-57.2, -35.6, -55, -34.7),
    "Lake Victoria (Kenya/Uganda/Tanzania)": ee.Geometry.BBox(31.7, -2.5, 34.2, 0.3),
    "Strait of Gibraltar": ee.Geometry.BBox(-6, 35.8, -5.2, 36.1),
    "Lake Melar (Sweden)": ee.Geometry.BBox(17.3, 59.3, 17.6, 59.5),
    "Gulf of Finland": ee.Geometry.BBox(24.8, 59.6, 28.8, 60.15),
    "Port of Rotterdam": ee.Geometry.BBox(3.9, 51.8, 4.5, 52.0),
    "Singapore Strait": ee.Geometry.BBox(103.6, 1.1, 104.1, 1.35),
    "Persian Gulf": ee.Geometry.BBox(48.1, 27, 50, 30.0),
    "Hong Kong": ee.Geometry.BBox(113.8, 21.7, 115, 22.3),
    "Port of Antwerp": ee.Geometry.BBox(4.2, 51.25, 4.4, 51.4),
    "Strait of Hormuz": ee.Geometry.BBox(56.3, 25, 57.2, 26.5),
}

def get_region(region_name):
    return region_geoms[region_name]

def calculate_center(region: ee.geometry.Geometry):
    bounds = region.bounds()
    coords = bounds.coordinates().get(0).getInfo()

    min_lon = coords[0][0]
    min_lat = coords[0][1]
    max_lon = coords[2][0]
    max_lat = coords[2][1]
    
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2
    
    return [center_lon, center_lat]

def combine_regions():
    combined_geom = None
    for geom in region_geoms.values():
        if combined_geom is None:
            combined_geom = geom
        else:
            combined_geom = combined_geom.union(geom,  ee.ErrorMargin(1))
    return combined_geom
