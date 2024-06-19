import ee
import math
import pandas as pd
import json

def read_points_from_ship_mask(region: ee.geometry.Geometry, dilated_ships_layer: ee.image.Image) -> ee.FeatureCollection:
    """
    #region = ee.Geometry.BBox(18.58, 54.69, 19.79, 54.34)
    #region = ee.Geometry.BBox(lg[0], lg[1], pd[0], pd[1])
    """
    bounds = region.bounds()
    coordinates = bounds.coordinates().get(0).getInfo()
    #[[18.58, 54.34], [19.79, 54.34], [19.79, 54.69], [18.58, 54.69], [18.58, 54.34]]
    lg_0 = coordinates[0][0]
    lg_1 = coordinates[2][1]
    pd_0 = coordinates[1][0]
    pd_1 = coordinates[0][1]
    #cords = region.getInfo()['coordinates'][0]
    #lg=cords[1]
    #pd=cords[3]
    #rozp_row = pd[0] - lg[0]
    #rozp_pol = lg[1] - pd[1]
    rozp_row = pd_0 - lg_0
    rozp_pol = lg_1 - pd_1
    rozp_row_d = rozp_row
    rozp_pol_d = rozp_pol
    rozp_row = rozp_row*10 #jak mnozysz *10 to wtedy iteruje co 0.1 stopnia 
    rozp_pol = rozp_pol*10
    rozp_row = math.ceil(rozp_row)
    rozp_pol = math.ceil(rozp_pol)

    all_points = ee.FeatureCollection([])

    for rozp_row_add in range(0, rozp_row):
        for rozp_pol_add in range(0, rozp_pol):
        
            #region = ee.Geometry.BBox(lg[0]+rozp_row_add/10, lg[1]-rozp_pol_add/10, lg[0]+rozp_row_add/10+0.1, lg[1]-rozp_pol_add/10-0.1)
            region = ee.Geometry.BBox(lg_0+rozp_row_add/10, lg_1-rozp_pol_add/10, lg_0+rozp_row_add/10+0.1, lg_1-rozp_pol_add/10-0.1)

            central_points = dilated_ships_layer.reduceToVectors(
                geometryType='centroid',
                reducer=ee.Reducer.countEvery(),
                scale=30,
                geometry=region 
            )
            all_points = all_points.merge(central_points)

    return all_points

def extract_points_to_list(central_points: ee.FeatureCollection) -> list:
    coordinates_list = []
    features = central_points.getInfo()['features']
    for index, feature in enumerate(features):
        coordinates = feature['geometry']['coordinates']
        coordinates_list.append({"latitude": coordinates[1], "longitude": coordinates[0], "name": f"Ship {index}"})
    return coordinates_list

def coordinates_to_geojson(ship_coordinates):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for ship in ship_coordinates:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [ship["longitude"], ship["latitude"]]
            },
            "properties": {
                "name": ship["name"]
            }
        }
        geojson["features"].append(feature)

    return json.dumps(geojson)

# Funkcja do pobrania danych jako plik CSV
def download_ship_coordinates(ship_coordinates):
    df = pd.DataFrame(ship_coordinates)
    return df.to_csv(index=False).encode('utf-8')
