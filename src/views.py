import streamlit as st
import geemap.foliumap as geemap
import ee
from ship_detection import layout, authenticate, detecting, extract_points, regions

# uruchamianie widoku Streamlit
def main():
    if 'global_map' not in st.session_state:
        st.session_state.global_map = None
    if 'map' not in st.session_state:
        st.session_state.map = layout.prepare_basemap()
    
    st.set_page_config(layout="wide")
    st.title("Ship Detection Application")

    with st.sidebar:
        # wybór daty
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        region = st.selectbox(
            "Region",
            (sorted(list(regions.region_geoms.keys()))),
            index=None, 
            placeholder="Select region..."
        )

        st.write("You selected:", region)

        generate_map = st.button("Generate Map")
        download_coordinates = st.button("Download ships coordinates")

    if generate_map:
        if start_date and end_date and region:
            st.write(f"Select SAR images from date range: {start_date} to {end_date}")
            map_or_error = run((str(start_date), str(end_date)), region)
            if isinstance(map_or_error, str):
                st.error(map_or_error)
            else:
                st.session_state.map = map_or_error
        else:
            st.session_state.global_map = layout.prepare_basemap()
            st.session_state.map = layout.prepare_basemap()

    if download_coordinates:
        if region:
            st.write("Starting point extraction...")
            points = extract_points.read_points_from_ship_mask(regions.get_region(region), st.session_state.global_map)
            st.write("Converting points...")
            points_list = extract_points.extract_points_to_list(points)
            csv_data = extract_points.download_ship_coordinates(points_list)
            geo_json_data = extract_points.coordinates_to_geojson(points_list).encode('utf-8')
            with st.sidebar:
                st.download_button(label="Download ships coordinates as CSV", data=csv_data, file_name=f'{region.replace(" ", "_")}_{start_date}_{end_date}.csv', mime='text/csv')
                st.download_button(label="Download ships coordinates as GeoJSON", data=geo_json_data, file_name=f'{region.replace(" ", "_")}_{start_date}_{end_date}.geojson', mime='application/json')
        else:
            st.error("Please select region")

    if st.session_state.map:
        st.session_state.map.to_streamlit(height=650)

# generowanie mapy
def run(date, region):
    credentials = authenticate.authorize()
    ee.Initialize(credentials)
    geemap.ee_initialize()

    try:
        if region:
            region_geom = regions.get_region(region)
            map = layout.prepare_map(date, region_geom)
            st.session_state.global_map = detecting.ships(date, region_geom)
            edges_with_none = detecting.canny_edge_detector(date, region_geom)
            center = regions.calculate_center(regions.get_region(region))
            map.setCenter(center[0], center[1], 9)
            map.addLayer(edges_with_none, {'palette': ['FF0000']}, 'Detected Ships')
        else:
            map = layout.prepare_basemap()
        return map

    except Exception as e:
        return f"Error: No images available for the given date range. Details: {e}."


if __name__ == "__main__":
    main()

