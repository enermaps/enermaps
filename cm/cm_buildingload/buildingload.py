# -*- coding: utf-8 -*-
"""
@author: ewilczynski
"""
import pandas as pd
import datetime
import xarray as xr
import time
import pvlib
import math
import numpy as np
#import rasterio
import logging
from pathlib import Path
from typing import Dict, Tuple
from BaseCM.cm_output import validate
from shapely.geometry import Polygon, Point, MultiPolygon
import shapefile

DECIMALS = 3
CURRENT_FILE_DIR = Path(__file__).parent
TESTDATA_DIR = CURRENT_FILE_DIR / "testdata"

def compute_centroid(geojson: Dict) -> Tuple[float, float]:
    try:
        coords = np.array(geojson["features"][0]["geometry"]["coordinates"])
    except KeyError:
        logging.error(geojson)
        raise ValueError(
            "FAILED! The provided geometry is not a correct/supported geojson format."
        )
    return tuple(np.around(coords[0].mean(0), decimals=DECIMALS))

def countrycode(
#        geojson: Dict,
        lon: float,
        lat: float):
    # Read shapefile
    path = 'Input/countries.shp'
    sf = shapefile.Reader(path)
    
    country_list = ['Austria', 'Bosnia and Herzegovina', 'Belgium', 'Bulgaria', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 'Spain', 'France', 'Great Britain', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Netherlands', 'Norway', 'Poland', 'Serbia', 'Sweden', 'Slovenia']
    countrycode_list = ['AT', 'BA', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'ES', 'FR', 'GB', 'GR', 'HU', 'IE', 'IT', 'NL', 'NO', 'PL', 'RS', 'SE', 'SI']
    n_countries = len(country_list)
    index = 0
    id_country = False

    while index < n_countries:
        shape_records = sf.shapeRecords()
        desired_shapes = []
        for s in shape_records:
            if s.record[1] == country_list[index]:
                desired_shapes.append(s.shape)
            polygon = desired_shapes
            shpfilePoints = [shape.points for shape in polygon]
            polygons = shpfilePoints
        for polygon in polygons:
            poly = Polygon(polygon)
        p1 = Point(lon, lat)
    
        #country_name = country_list[index]
        country_code = countrycode_list[index]
        
        if p1.within(poly) == True:
            id_country = True
            break
        else:
            index += 1
        
    if id_country == True:
        return country_code
    else:
        print("Location not in compatible location")

def buildingload(
        geojson: Dict,
        building_type: str = "SFH",
        construction_year: int = 2020,
        gfa_external: float = 100.00,
        n_stories: int = 1,
        t_set_min: float = 20.0,
        t_set_max: float = 26.0,
        user_month: str = "January",
        user_week: str = "Week 1",
        user_day: str = "Monday",
        user_model_length: str = "Day",
        roof_type_orientation: str = "0",
        user_roof_pitch: float = 30.0,
        w_f_r: float = 1.3,
        L: int = 1,
        W: int = 1,
        facade_orientation: str = "north",
        a_door: float = 2.0,
        window_front_proportion: float = 10.0,
        window_back_proportion: float = 25.0,
        window_side_1_proportion: float = 25.0,
        window_side_2_proportion: float = 25.0
        ):
    
    lon, lat = compute_centroid(geojson)
    #lon = 11.4041
    #lat = 47.2692
    # Latitude / longitude
    user_lat = lat
    user_long = lon
    
    # Load Tabula/Episcope data
    df_tabula = pd.read_excel('Input/tabula-calculator.xlsx', sheet_name='Calc.Set.Building', skiprows=[1,2,3,4,5,6,7,8,9], engine='openpyxl')
    # Load weather data
    ds_weather = xr.open_dataset("Input/copernicus_weather.nc")
    ds_weather_loc = ds_weather.sel(latitude=user_lat, longitude=user_long, method="nearest")
    df_weather_loc = ds_weather_loc.to_dataframe()
    ds_humidity = xr.open_dataset("Input/copernicus_pressurelevels.nc")
    ds_humidity_loc = ds_humidity.sel(latitude=user_lat, longitude=user_long, method="nearest")
    df_humidity_loc = ds_humidity_loc.to_dataframe()
    humidity_join = df_humidity_loc["r"]
    df_weather = df_weather_loc.join(humidity_join)
    
    country_code = countrycode(lon=lon, lat=lat)
    
    # Unrestricted heating power (W/m2)
    heating_power = 10
    
    # Tabula row selection prep
    if country_code == "GB":
        refcode1 = "ENG"
    elif country_code == "GR":
        refcode1 = "ZoneA"
    elif country_code == "IT":
        refcode1 = "MidClim"    
    else:
        refcode1 = "N"

    # Get building class period from construction year
    building_class = df_tabula[(df_tabula['Year2_Building'] > construction_year) & (df_tabula['Year1_Building'] < construction_year) & (df_tabula['Code_Country'] == country_code) & (df_tabula['Code_BuildingSizeClass'] == building_type)]
    building_class = building_class['Code_ConstructionYearClass'].iloc[0][3:]
    
    # Select Tabula row/building
    tabula_row = str(country_code) + "." + str(refcode1) + "." + str(building_type) + "." + str(building_class) + ".Gen.ReEx.001.001"
    df_tabula_row = df_tabula[df_tabula['Code_BuildingVariant'] == tabula_row]
    
    
    # Parameters
    pm = {
            # Parameter for calculating effective mass area, A_m (Table 12)
            "A_m_parameter": 2.5,
            # Parameter for internal heat capacity, C_m (Table 12)
            "C_m_parameter": df_tabula_row["c_m"] * 3600, 
            # Reduction factor external shading, horizontal orientation
            "F_sh_hor": df_tabula_row["F_sh_hor"],
            # Reduction factor external shading, vertical orientations
            "F_sh_vert": df_tabula_row["F_sh_vert"],
            # Form factor for radiation between the element and the sky for unshaded horizontal roof
            "F_r_hor": 1.0,
            # Form factor for radiation between the element and the sky for unshaded vertical roof
            "F_r_vert": 0.5,
            # U value of wall 1 
            "u_wall_1": df_tabula_row["U_Wall_1"],
            # Adjustment factor wall 1        
            "tf_wall_1": df_tabula_row["b_Transmission_Wall_1"],          
            # U value of roof 1
            "u_roof_1": df_tabula_row["U_Roof_1"],
            # U value of roof 2
            "u_roof_2": df_tabula_row["U_Roof_1"],
            # Adjustment factor roof 1        
            "tf_roof_1": df_tabula_row["b_Transmission_Roof_1"],
            # U value of Door
            "u_door_1": df_tabula_row["U_Door_1"],
            # U value of window 1
            "u_window_1": df_tabula_row["U_Window_1"],         
            # Standard room height
            "h_room": df_tabula_row["h_room"],
            # Heat transfer coefficient between the air node and surface node (W/(m²K))
            "h_is": 3.45,
            # Dimensionless ratio between the internal surfaces area and the floor area
            "lambda_at": 4.5,
            # Heat transfer coefficient between nodes m and s
            "h_ms": 9.1,
            # Heat capacity of air per volume (J/(m^3 K))
            "rho_a_c_a": 1200,
            # Average heat flow per person (W/person)
            "Q_P": 70,
            # Frame area fraction
            "F_F": 0.3,
            # Frame area fraction
            "F_w": 0.9,
            # Total solar energy transmittance for radiation perpendicular to the glazing
            "g_gl_n": df_tabula_row["g_gl_n"],
            # Air change rate from infiltration (per hour) 
            "n_air_inf": df_tabula_row["n_air_infiltration"],
            # Air change rate from use (per hour)
            "n_air_use": df_tabula_row["n_air_use"],  
            # Dimensionless absorption coefficient for solar radiation of the opaque part
            "alpha_S_c": 0.6,
            # Average difference between the external air temperature and the apparent sky temperature (degC)
            "delta_theta_er": 11,
            # Arithmetic average of the surface temperature and the sky temperature (degC)
            "theta_ss": 11,
            # Stefan-Boltzmann constant (W/(m^2 * K^4))
            "SB_constant": 5.67 * (10**-8),
            # Emissivity of external opaque elements (roof, wall)
            "epsilon_op": 0.9,
            # Emissivity of external glazed elements (window, door)
            "epsilon_gl": 0.9,
            # External surface heat resistance of the opaque part (ISO 6946)
            "R_S_e_op": 0.04,
             # External surface heat resistance of the glazed part (Tabula)
            "R_S_e_gl": df_tabula_row["R_Before_Window_1"],      
            # Parameter for calculation of conditioned floor area (from Tabula calculations)
            "gfa_parameter": 0.85,
            # U values for walls
            "u_wall_north": df_tabula_row["U_Wall_1"],
            "u_wall_east": df_tabula_row["U_Wall_1"],
            "u_wall_south": df_tabula_row["U_Wall_1"],
            "u_wall_west": df_tabula_row["U_Wall_1"]
            }
    global a_window_north, a_window_south, a_window_west, a_window_east, a_door_1, a_roof_1, a_roof_2, a_wall_north, a_wall_south, a_wall_east, a_wall_west
    
    # User defined:
    # Interior gross floor area
    # / Create logic to match with tabula structure due to use of other values (e.g., roof area)
    gfa_interior = gfa_external * pm["gfa_parameter"] * n_stories
    
    # Configure external elements
    # Orientation values
    orientation_lib = ["north","east","south","west"]
    
    # Calculate external wall area
    a_wall_ext = w_f_r * gfa_external * n_stories
    # Calculate building external wall areas based on shape (NOTE: wall side_1 is left wall when facing facade)
    a_external_front = ((W/(L+W)) * a_wall_ext)/2
    a_external_back = ((W/(L+W)) * a_wall_ext)/2
    a_external_side_1 = ((L/(L+W)) * a_wall_ext)/2
    a_external_side_2 = ((L/(L+W)) * a_wall_ext)/2
    
    a_door_1 = a_door
        
    # Ensure flat roof has 0 degree pitch
    if roof_type_orientation == 6:
        roof_pitch = 0
    else:
        roof_pitch = user_roof_pitch
    # Calculate roof area based on external structure area and pitch
    a_roof_total = gfa_external / np.cos(roof_pitch)
    
    # Calculate area of window
    a_window_front = (window_front_proportion/100) * (a_external_front - a_door_1)
    a_window_back = (window_back_proportion/100) * a_external_back
    a_window_side_1 = (window_side_1_proportion/100) * a_external_side_1
    a_window_side_2 = (window_side_2_proportion/100) * a_external_side_2
    
    # Calculate area of external walls
    a_wall_front = a_external_front - a_window_front - a_door_1
    a_wall_back = a_external_back - a_window_back
    a_wall_side_1 = a_external_side_1 - a_window_side_1
    a_wall_side_2 = a_external_side_2 - a_window_side_2
    
    if facade_orientation == "north":
        door_1_azimuth = 0.0
        a_window_north = a_window_front
        a_window_south = a_window_back
        a_window_west = a_window_side_1
        a_window_east = a_window_side_2
        a_wall_north = a_wall_front
        a_wall_south = a_wall_back
        a_wall_west = a_wall_side_1
        a_wall_east = a_wall_side_2
        print(a_window_north)
    elif facade_orientation == "south":
        door_1_azimuth = 180.0
        a_window_south = a_window_front
        a_window_north = a_window_back
        a_window_east = a_window_side_1
        a_window_west = a_window_side_2
        a_wall_south = a_wall_front
        a_wall_north = a_wall_back
        a_wall_east = a_wall_side_1
        a_wall_west = a_wall_side_2
    elif facade_orientation == "east":
        door_1_azimuth = 90.0
        a_window_east = a_window_front
        a_window_west = a_window_back
        a_window_north = a_window_side_1
        a_window_south = a_window_side_2
        a_wall_east = a_wall_front
        a_wall_west = a_wall_back
        a_wall_north = a_wall_side_1
        a_wall_south = a_wall_side_2    
    else:
        door_1_azimuth = 270.0
        a_window_west = a_window_front
        a_window_east = a_window_back
        a_window_south = a_window_side_1
        a_window_north = a_window_side_2
        a_wall_west = a_wall_front
        a_wall_east = a_wall_back
        a_wall_south = a_wall_side_1
        a_wall_north = a_wall_side_2
    
    # Roof type, tilt, and orientation
    if roof_type_orientation == "0":
        roof_1_azimuth = 0.0
        roof_2_azimuth = 180.0
        a_roof_1 = a_roof_total/2
        a_roof_2 = a_roof_total/2
    elif roof_type_orientation == "1":
        roof_1_azimuth = 90.0
        roof_2_azimuth = 270.0    
        a_roof_1 = a_roof_total/2
        a_roof_2 = a_roof_total/2
    elif roof_type_orientation == "2":
        roof_1_azimuth = 0.0
        roof_2_azimuth = 0.0
        a_roof_1 = a_roof_total
        a_roof_2 = 0.0
    elif roof_type_orientation == "3":
        roof_1_azimuth = 90.0
        roof_2_azimuth = 90.0
        a_roof_1 = a_roof_total
        a_roof_2 = 0.0
    elif roof_type_orientation == "4":
        roof_1_azimuth = 180.0
        roof_2_azimuth = 180.
        a_roof_1 = a_roof_total
        a_roof_2 = 0.0
    elif roof_type_orientation == "5":
        roof_1_azimuth = 270.0
        roof_2_azimuth = 270.0
        a_roof_1 = a_roof_total
        a_roof_2 = 0.0
    elif roof_type_orientation == "6":
        roof_1_azimuth = 0.0
        roof_2_azimuth = 0.0
        a_roof_1 = a_roof_total
        a_roof_2 = 0.0
    else:
        print("Invalid Roof Type/Orientation code")
    
    
    element = ["window_north","window_east","window_south","window_west","door_1","roof_1","roof_2","wall_north","wall_east","wall_south","wall_west"]
    azimuth_lib = {"north": 0.0,"east": 90.0,"south": 180.0,"west": 270.0,"door_1": door_1_azimuth,"roof_1": roof_1_azimuth,"roof_2": roof_2_azimuth}
    tilt_lib = {"north": 90.0,"east": 90.0,"south": 90.0,"west": 90.0,"door_1": 90.0,"roof_1": roof_pitch,"roof_2": roof_pitch}   
    
    
    # Set temperatures for heating and cooling
    theta_int_C_set = t_set_max
    theta_int_H_set = t_set_min
    # Maximum heating and cooling power EJW OK?
    phi_H_max = float("inf")
    phi_C_max = -float("inf") 
    #phi_H_max = 100
    #phi_C_max = -100
    
    # Conditioned floor area (m2)
    A_f = gfa_interior
    # Effective mass area (m2)
    A_m = pm["A_m_parameter"] * A_f
    # Thermal capacitance of medium (J/K)
    C_m = pm["C_m_parameter"] * A_f
    # Area of all surfaces facing the building zone (m2)
    A_tot = pm["lambda_at"] * A_f
    A_t = A_tot
    # Coupling conductance between air and surface nodes (W/K)
    H_tr_is = pm["h_is"] * A_tot
    
    # Ventilation heat transfer coefficients
    # Total air changes (1/h)
    n_air_total = pm["n_air_inf"] + pm["n_air_use"]
    # Air volume of room (m3)
    air_volume = pm["h_room"] * A_f
    # Temperature adjustment factor for the air flow element
    b_ve = 1
    # Time fraction of operation of the air flow element (f_ve_t = 1 assumes element is always operating)
    # E.g. If only operating from 8.00 to 18.00, then f_ve_t = 10 hours/24 hours = 0.417
    f_ve_t = 1
    # Airflow rate of the air flow element (m3/s)
    q_ve = n_air_total/3600 * air_volume
    # Time-average airflow rate of the air flow element (m3/s)
    q_ve_mn = f_ve_t * q_ve
    # Ventilation heat transfer coefficient (W/K)
    H_ve_adj = pm["rho_a_c_a"] * b_ve * q_ve_mn
    # Combined heat conductance (W/K)
    H_tr_1 = 1 / (1/H_ve_adj + 1/H_tr_is)
    
    # Heat transfer opaque elements (walls and roof) (W/K)
    H_tr_op = (a_wall_front + a_wall_back + a_wall_side_1 + a_wall_side_2) * pm["u_wall_1"] * pm["tf_wall_1"] + a_roof_total * pm["u_roof_1"] * pm["tf_roof_1"]
    # Thermal transmission coefficient of glazed elements (windows and doors) (W/K)
    H_tr_w = a_window_front * pm["u_window_1"] + a_window_back * pm["u_window_1"] + a_window_side_1 * pm["u_window_1"] + a_window_side_2 * pm["u_window_1"] + a_door_1 * pm["u_door_1"]
    # Split H_tr_op into coupling conductance between nodes m and s (W/K)
    H_op = H_tr_op
    H_ms = pm["h_ms"] * A_m
    H_em = 1/(1/H_op - 1/H_ms)
    H_tr_ms = H_ms
    H_tr_em = H_em
    
    # External radiative heat transfer coefficient for opaque and glazed surfaces (W/(m²K))
    h_r_op = 4 * pm["epsilon_op"] * pm["SB_constant"] * ((pm["theta_ss"] + 273)**3)
    h_r_gl = 4 * pm["epsilon_gl"] * pm["SB_constant"] * ((pm["theta_ss"] + 273)**3)
    
    
    #start_date = datetime.datetime(2017,1,1,0) #EJW change to 2017
    #end_date = datetime.datetime(2017,1,31,23) #EJW change to 2017
    
    year_set = 2017
    month_lib = {"January": 1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    
    # Set up date/time and list of inputs/outputs for calculaton
    if user_model_length == "Day":
        if user_week == "Week 1":
            week_start = 7
        elif user_week == "Week 2":
            week_start = 14
        elif user_week == "Week 3":
            week_start = 21
        d = datetime.datetime(year_set, month_lib[user_month], week_start)
        d_offset = -d.weekday()
        first_monday_date = d + datetime.timedelta(d_offset)
        first_monday = first_monday_date .day
        if user_day == "Monday":
            start_date = datetime.datetime(year_set,month_lib[user_month],first_monday,0)
        elif user_day == "Tuesday":
            start_date = datetime.datetime(year_set,month_lib[user_month],(first_monday+1),0)
        elif user_day == "Wednesday":
            start_date = datetime.datetime(year_set,month_lib[user_month],(first_monday+2),0)
        elif user_day == "Thursday":
            start_date = datetime.datetime(year_set,month_lib[user_month],(first_monday+3),0)
        elif user_day == "Friday":
            start_date = datetime.datetime(year_set,month_lib[user_month],(first_monday+4),0)
        elif user_day == "Saturday":
            start_date = datetime.datetime(year_set,month_lib[user_month],(first_monday+5),0)
        elif user_day == "Sunday":
            start_date = datetime.datetime(year_set,month_lib[user_month],(first_monday+6),0)
        end_date = start_date + datetime.timedelta(hours=23)
    elif user_model_length == "Week":
        if user_week == "Week 1":
            week_start = 7
        elif user_week == "Week 2":
            week_start = 14
        elif user_week == "Week 3":
            week_start = 21
        d = datetime.datetime(year_set, month_lib[user_month], week_start)
        d_offset = -d.weekday()
        first_monday_date = d + datetime.timedelta(d_offset)
        first_monday = first_monday_date .day
        start_date = datetime.datetime(year_set,month_lib[user_month],first_monday,0)
        end_date = start_date + datetime.timedelta(days=6, hours=23)
    elif user_model_length == "Month":
        start_date = datetime.datetime(year_set,month_lib[user_month],1,0)
        end_date = start_date + datetime.timedelta(Month=1) - datetime.timedelta(hours=1)
    else:
        start_date = datetime.datetime(year_set,month_lib[user_month],1,0)
        end_date = datetime.datetime(year_set,month_lib[user_month],31,23)
        
    delta = datetime.timedelta(hours=1)
    time_length = end_date - start_date
    cols = ['hour_of_day','day_of_week','t_outside_t2m','t_outside_d2m','humidity','surface_pressure','ghi','dni','dhi','solar_position','relative_airmass','extra_radiation','solar_altitude','solar_altitude_radians','solar_azimuth','solar_azimuth_radians','solar_zenith','solar_zenith_radians','total_irradiance','phi_int','phi_sol','Q_HC_nd','Q_H_nd','Q_C_nd','theta_air','t_outside_t2m_degC','theta_air_ac', 'i_sol', 'theta_air_0', 'theta_air_10', 'theta_m_tp', 'theta_m_t', 'dmt']
    n_timesteps = int(time_length.total_seconds() / delta.total_seconds())
    year = start_date. year
    timestamp_list = [(start_date + x*delta) for x in range(0,n_timesteps+1)]
    df = pd.DataFrame(columns=cols,index=timestamp_list)
    current_timestamp = start_date
    current_index = 0
    
    # Initial theta_m_t value
    theta_m_t = 12
    # Initial theta_air
    theta_air_ac = 12
    theta_air = theta_air_ac
    theta_m_tp_list = []
    theta_m_tp_list.append(theta_m_t) #EJW mtp
    # RC simulation
    while current_timestamp <= end_date:
        
        print(current_timestamp)
        #df.dmt[current_index] = current_timestamp.time().strftime('%H:%M:%S')
        df.dmt[current_index] = current_timestamp.time().strftime('%b %d %H:%M:%S')
        df.dmt[current_index] = str(df.dmt[current_index])
        print('Loading weather variables')
        # Set weather variables
        # Outside dry bulb temperature (K)
        df.t_outside_t2m[current_index] = df_weather.t2m[current_index]
        t_outside_t2m = df.t_outside_t2m[current_index]
        # Outside dry bulb temperature (deg C)
        df.t_outside_t2m_degC[current_index] = t_outside_t2m - 273.15
        # Outside dew point temperature (K)
        df.t_outside_d2m[current_index] = df_weather.d2m[current_index]
        t_outside_d2m = df.t_outside_d2m[current_index]
        # Outside dew point temperature (deg C)
        t_outside_d2m_degC = t_outside_d2m - 273.15
        # Relative humidity
        df.humidity[current_index] = df_weather.r[current_index]
        # Surface pressure
        df.surface_pressure[current_index] = df_weather.sp[current_index]
        # Surface Solar Radiation Downwards (SSRD): Global Horizontal Irradiance (GHI)
        df.ghi[current_index] = df_weather.ssrd[current_index]
        ghi = df.ghi[current_index] / 3600 # Convert from J/m2 to W/m2
        # Direct solar radiation at the surface (FDIR): Direct Normal Irradiance (DNI)
        df.dni[current_index] = df_weather.fdir[current_index]
        dni = df.dni[current_index] / 3600 # Convert from J/m2 to W/m2
        # (SSRD - FDIR): Diffuse Horizontal Irradiance (DHI)
        df.dhi[current_index] = df_weather.ssrd[current_index] - df_weather.fdir[current_index]
        dhi = df.dhi[current_index] / 3600 # Convert from J/m2 to W/m2
               
        print('    Finished loading weather variables')
        print('Getting values from pvlib')
        # Convert lat/long to radians for pvlib
        latitude_radians = math.radians(user_lat)
        longitude_radians = math.radians(user_long)
        # Solar position
        df.solar_position[current_index] = pvlib.solarposition.get_solarposition(current_timestamp, user_lat, user_long, pressure=df.surface_pressure[current_index], temperature=df.t_outside_t2m_degC[current_index])
        solar_position = df.solar_position[current_index]
        # Solar altitude
        df.solar_altitude[current_index] = solar_position["apparent_elevation"]
        solar_altitude = df.solar_altitude[current_index]
        # Solar azimuth
        df.solar_azimuth[current_index] = solar_position["azimuth"]
        solar_azimuth = df.solar_azimuth[current_index]
        # Solar zenith
        df.solar_zenith[current_index] = solar_position["apparent_zenith"]
        solar_zenith = df.solar_zenith[current_index]
        # Airmass
        df.relative_airmass[current_index] = pvlib.atmosphere.get_relative_airmass(solar_zenith)
        relative_airmass = df.relative_airmass[current_index]
        # Extra DNI
        df.extra_radiation[current_index] = pvlib.irradiance.get_extra_radiation(current_timestamp.timetuple().tm_yday, epoch_year = current_timestamp. year)
        dni_extra = df.extra_radiation[current_index]     
        print('    Finished getting values from pvlib')
        
        print('Calculating solar gains') 
        
        # Calculates values for the form factor for radiation between the unshaded roof and the sky
        F_r_roof = 1 - roof_pitch/180
        # Solar radiation and gains results storage
        phi_sol_results = []
        i_sol_results = []
        for i in azimuth_lib:
            surface_azimuth = azimuth_lib[i]
            surface_tilt = tilt_lib[i]
            I_sol_element = pvlib.irradiance.get_total_irradiance(
                        surface_tilt,
                        surface_azimuth,
                        solar_zenith,
                        solar_azimuth,
                        dni=dni,
                        ghi=ghi,
                        dhi=dhi,
                        dni_extra=dni_extra,
                        airmass=relative_airmass,
                        model="perez",
                        surface_type="urban")
            # Irradiance on element (W/m2)
            globals()[f"I_sol_{i}"] = float(I_sol_element["poa_global"].fillna(0))
            i_sol_results.append(float(globals()[f"I_sol_{i}"]))
        
        global i_sol_window_north, i_sol_window_east, i_sol_window_west, i_sol_window_south, i_sol_door_1, i_sol_roof_1, i_sol_roof_2, i_sol_wall_north, i_sol_wall_south, i_sol_wall_east, i_sol_wall_west
        i_sol_window_north = float(i_sol_results[0])
        i_sol_window_east = float(i_sol_results[1])
        i_sol_window_south = float(i_sol_results[2])
        i_sol_window_west = float(i_sol_results[3])
        i_sol_door_1 = float(i_sol_results[4])
        i_sol_roof_1 = float(i_sol_results[5])
        i_sol_roof_2 = float(i_sol_results[6])
        i_sol_wall_north = float(i_sol_results[0])
        i_sol_wall_east = float(i_sol_results[1])
        i_sol_wall_south = float(i_sol_results[2])
        i_sol_wall_west = float(i_sol_results[3])
               
        for i in element:
            element_name_a = "a_" + i
            element_area = globals()[f"a_{i}"]
            g_gl = pm["F_w"] * pm["g_gl_n"]
            if (i == "window_north") | (i == "window_east") | (i == "window_south") | (i == "window_west"):
                element_name_i_sol = "i_sol_" + i
                i_sol_window = element_name_i_sol
                # Shading reduction factor for movable shading provisions
                F_sh_gl = pm["F_sh_vert"]
                element_u = pm["u_window_1"]  
                element_r = pm["R_S_e_gl"]
                # Effective solar collecting area of element
                globals()[f"A_sol_{i}"] = F_sh_gl * g_gl * (1 - pm["F_F"]) * element_area
                # Thermal radiation heat flow to the sky (W)
                globals()[f"phi_r_{i}"] = element_r * element_u * element_area * h_r_gl * pm["delta_theta_er"]
                # Heat flow by solar gains through building element
                globals()[f"phi_sol_{i}"] = pm["F_sh_vert"] * globals()[f"A_sol_{i}"] * globals()[f"i_sol_{i}"] - pm["F_r_vert"] * globals()[f"phi_r_{i}"]
                if float(globals()[f"phi_sol_{i}"]) < 0:
                    globals()[f"phi_sol_{i}"] = 0
                phi_sol_results.append(float(globals()[f"phi_sol_{i}"]))
            elif (i == "door_1"):
                # Shading reduction factor for movable shading provisions
                F_sh_gl = pm["F_sh_vert"]
                element_name_u = "u_" + i
                element_u = pm[element_name_u]
                element_r = pm["R_S_e_gl"]
                # Effective solar collecting area of element
                globals()[f"A_sol_{i}"] = F_sh_gl * g_gl * (1 - pm["F_F"]) * element_area
                # Thermal radiation heat flow to the sky (W)
                globals()[f"phi_r_{i}"] = element_r * element_u * element_area * h_r_gl * pm["delta_theta_er"]
                # Heat flow by solar gains through building element
                globals()[f"phi_sol_{i}"] = pm["F_sh_vert"] * globals()[f"A_sol_{i}"] * i_sol_door_1 - pm["F_r_vert"] * globals()[f"phi_r_{i}"]
                if float(globals()[f"phi_sol_{i}"]) < 0:
                    globals()[f"phi_sol_{i}"] = 0
                phi_sol_results.append(float(globals()[f"phi_sol_{i}"]))
            elif (i == "roof_1") | (i == "roof_2"):
                element_name_i_sol = "i_sol_" + i
                i_sol_roof = element_name_i_sol
                element_name_u = "u_" + i
                element_u = pm[element_name_u]
                element_r = pm["R_S_e_op"]
                # Effective solar collecting area of element
                globals()[f"A_sol_{i}"] = pm["alpha_S_c"] * element_r * element_u * element_area
                # Thermal radiation heat flow to the sky (W)
                globals()[f"phi_r_{i}"] = element_r * element_u * element_area * h_r_op * pm["delta_theta_er"]
                # Heat flow by solar gains through building element
                globals()[f"phi_sol_{i}"] = pm["F_sh_hor"] * globals()[f"A_sol_{i}"] * globals()[f"I_sol_{i}"] - F_r_roof * globals()[f"phi_r_{i}"]
                if float(globals()[f"phi_sol_{i}"]) < 0:
                    globals()[f"phi_sol_{i}"] = 0
                phi_sol_results.append(float(globals()[f"phi_sol_{i}"]))
            elif (i == "wall_north") | (i == "wall_east") | (i == "wall_south") | (i == "wall_west"):
                element_name_u = "u_" + i
                element_u = pm[element_name_u]
                element_r = pm["R_S_e_op"]
                # Effective solar collecting area of element 
                globals()[f"A_sol_{i}"] = pm["alpha_S_c"] * element_r * element_u * element_area
                # Thermal radiation heat flow to the sky (W)
                globals()[f"phi_r_{i}"] = element_r * element_u * element_area * h_r_op * pm["delta_theta_er"]
                # Heat flow by solar gains through building element
                globals()[f"phi_sol_{i}"] = pm["F_sh_vert"] * globals()[f"A_sol_{i}"] * globals()[f"i_sol_{i}"] - pm["F_r_vert"] * globals()[f"phi_r_{i}"]
                if float(globals()[f"phi_sol_{i}"]) < 0:
                    globals()[f"phi_sol_{i}"] = 0
                phi_sol_results.append(float(globals()[f"phi_sol_{i}"]))
                      
        df.i_sol[current_index] = sum(i_sol_results)  #EJW (for observing results in output)
        df.phi_sol[current_index] = sum(phi_sol_results)   
        phi_sol = df.phi_sol[current_index]
        
        print('    Finished calculating solar gains')
        
        print('Calculating internal gains')
        #INTERNAL GAINS
        # From Table G.8
        # Check if weekday or weekend (Monday-Friday = 0-4, Saturday-Sunday = 5-6)
        # Adjust heat flow rate from occupants and appliances in living room and kitchen (hf_Oc_A_LRK)
        # Adjust heat flow rate from occupants and appliances in other rooms (e.g. bedrooms) (hf_Oc_A_Oth)
        df.day_of_week[current_index] = df.index[current_index].weekday()
        df.hour_of_day[current_index] = df.index[current_index].hour
        day_of_week = df.index[current_index].weekday()
        hour_of_day = df.index[current_index].hour    
        if ((day_of_week == 0) | (day_of_week == 1) | (day_of_week == 2) | (day_of_week == 3) | (day_of_week == 4)) & (7 <= hour_of_day <= 17):
            hf_Oc_A_LRK = 8
            hf_Oc_A_Oth = 1
        elif ((day_of_week == 0) | (day_of_week == 1) | (day_of_week == 2) | (day_of_week == 3) | (day_of_week == 4)) & (17 < hour_of_day <= 23):
            hf_Oc_A_LRK = 20
            hf_Oc_A_Oth = 1
        elif ((day_of_week == 0) | (day_of_week == 1) | (day_of_week == 2) | (day_of_week == 3) | (day_of_week == 4)) & (23 < hour_of_day < 7):
            hf_Oc_A_LRK = 2
            hf_Oc_A_Oth = 6
        elif ((day_of_week == 5) | (day_of_week == 6)) & (7 <= hour_of_day <= 17):
            hf_Oc_A_LRK = 8
            hf_Oc_A_Oth = 2
        elif ((day_of_week == 5) | (day_of_week == 6)) & (17 < hour_of_day <= 23):
            hf_Oc_A_LRK = 20
            hf_Oc_A_Oth = 4
        else:
            hf_Oc_A_LRK = 2
            hf_Oc_A_Oth = 6    
     
        # Heat flow rate for metabolic heat from occupants and dissipated heat from appliances (W)
        phi_int_Oc_A = (hf_Oc_A_LRK + hf_Oc_A_Oth) * A_f
        # Heat flow rate from internal sources (W)
        df.phi_int[current_index] = float(phi_int_Oc_A)
        phi_int = df.phi_int[current_index]
        # Heat flow rate to air (W)
        phi_ia = 0.5 * phi_int
        # Heat flow rate to internal surface (W)
        phi_st = (1 - (A_m / A_t) - (H_tr_w / (9.1 * A_t))) * (0.5 * phi_int + phi_sol)
        # Heat flow rate to medium (W)
        phi_m = (A_m / A_t) * (0.5 * phi_int + phi_sol)
        print('    Finished calculating internal gains')
        
        print('<<<Starting calculation for timestep>>>')
        # Set supply temperature equal to outside temperature
        theta_sup = df.t_outside_t2m_degC[current_index]
        
        # STEP 1
        # ------ 
        # Check if heating or cooling is needed:
        phi_HC_nd_0 = 0
        H_tr_2_0 = H_tr_1 + H_tr_w
        H_tr_3_0 = 1 / (1/H_tr_2_0 + 1/H_tr_ms)
        if current_index == 0:
            theta_m_tp_0 = 0
            theta_m_t_0 = 0
        else:
            theta_m_tp_0 = theta_m_t
        phi_mtot_0 = phi_m + H_tr_em * theta_sup + H_tr_3_0 * (phi_st + H_tr_w * theta_sup + H_tr_1 * (((phi_ia + phi_HC_nd_0)/H_ve_adj) + theta_sup)) / H_tr_2_0
        theta_m_tp_0 = theta_m_tp_list[0] #EJW mtp
        theta_m_t_0 = (theta_m_tp_0 * ((C_m/3600) - 0.5 * (H_tr_3_0 + H_tr_em)) + phi_mtot_0) / ((C_m/3600) + 0.5 * (H_tr_3_0 + H_tr_em))
        theta_m_0 = (theta_m_t_0 + theta_m_tp_0)/2
        theta_s_0 = (H_tr_ms * theta_m_0 + phi_st + H_tr_w * theta_sup + H_tr_1 * (theta_sup + (phi_ia + phi_HC_nd_0)/H_ve_adj)) / (H_tr_ms + H_tr_w + H_tr_1)
        df.theta_air_0[current_index] = (H_tr_is * theta_s_0 + H_ve_adj * theta_sup + phi_ia + phi_HC_nd_0) / (H_tr_is + H_ve_adj)
        theta_air_0 = float(df.theta_air_0[current_index])
        theta_op_0 = 0.3 * theta_air_0 + 0.7 * theta_s_0
    
        if (float(theta_air_0) >= theta_int_H_set) & (float(theta_air_0) <= theta_int_C_set):
            phi_HC_nd_ac = 0
            df.theta_air_ac[current_index] = float(theta_air_0)
            df.theta_air[current_index] = df.theta_air_ac[current_index]
            df.Q_HC_nd[current_index] = 0
            df.Q_H_nd[current_index] = 0
            df.Q_C_nd[current_index] = 0
            Q_int = phi_int * 0.036
            Q_sol = phi_sol * 0.036
            df.theta_m_t[current_index] = theta_m_t_0
            theta_m_t = theta_m_t_0
            theta_m_tp_list.clear() #EJW mtp
            theta_m_tp_list.append(theta_m_t) #EJW mtp
            current_timestamp += delta
            current_index += 1
            print('mark1')
            print('<<<End calculation for timestep, Case 3>>>')
            continue
        else:
            pass
            print('mark2')
    
        # STEP 2
        # ------ 
        if float(theta_air_0) > theta_int_C_set:
            theta_air_set = theta_int_C_set
            print('mark3')
        elif float(theta_air_0) < theta_int_H_set:
            theta_air_set = theta_int_H_set
            print('mark4')
            
        # Apply heating factor of 10 W/m2:
        phi_HC_nd_10 = A_f * heating_power
        H_tr_2_10 = H_tr_1 + H_tr_w
        H_tr_3_10 = 1 / (1/H_tr_2_10 + 1/H_tr_ms)
        if current_index == 0:
            theta_m_tp_10 = 0
            theta_m_t_10 = 0
        else:
            theta_m_tp_10 = theta_m_t
        phi_mtot_10 = phi_m + H_tr_em * theta_sup + H_tr_3_10 * (phi_st + H_tr_w * theta_sup + H_tr_1 * (((phi_ia + phi_HC_nd_10)/H_ve_adj) + theta_sup)) / H_tr_2_10
        theta_m_tp_10 = theta_m_tp_list[0] #EJW mtp
        theta_m_t_10 = (theta_m_tp_10 * ((C_m/3600) - 0.5 * (H_tr_3_10 + H_tr_em)) + phi_mtot_10) / ((C_m/3600) + 0.5 * (H_tr_3_10 + H_tr_em))
        theta_m_10 = (theta_m_t_10 + theta_m_tp_10)/2
        theta_s_10 = (H_tr_ms * theta_m_10 + phi_st + H_tr_w * theta_sup + H_tr_1 * (theta_sup + (phi_ia + phi_HC_nd_10)/H_ve_adj)) / (H_tr_ms + H_tr_w + H_tr_1)
        df.theta_air_10[current_index] = (H_tr_is * theta_s_10 + H_ve_adj * theta_sup + phi_ia + phi_HC_nd_10) / (H_tr_is + H_ve_adj)
        theta_air_10 = float(df.theta_air_10[current_index])
        theta_op_10 = 0.3 * theta_air_10 + 0.7 * theta_s_10
        # Unrestricted heating/cooling, phi_HC_nd_un, is positive for heating and negative for cooling 
        phi_HC_nd_un = (phi_HC_nd_10*(theta_air_set - theta_air_0))/(theta_air_10 - theta_air_0)
        
        # STEP 3
        # ------    
        if (float(phi_HC_nd_un) > phi_C_max) & (float(phi_HC_nd_un) < phi_H_max):
            phi_HC_nd_ac = float(phi_HC_nd_un)
            df.theta_air_ac[current_index] = theta_air_set
            df.theta_air[current_index] = df.theta_air_ac[current_index]
            # The energy need (MJ) for heating or cooling for a given hour, Q_HC_nd, is positive in the case of heating need and negative in the case of cooling need
            df.Q_HC_nd[current_index] = phi_HC_nd_ac / 1000
            df.Q_H_nd[current_index] = max(0, float(df.Q_HC_nd[current_index]))
            df.Q_C_nd[current_index] = abs(min(0, float(df.Q_HC_nd[current_index])))
            Q_int = phi_int * 0.036
            Q_sol = phi_sol * 0.036
            df.theta_m_t[current_index] = theta_m_t_10
            theta_m_t = theta_m_t_10
            theta_m_tp_list.clear() #EJW mtp
            theta_m_tp_list.append(theta_m_t) #EJW mtp
            current_timestamp += delta
            current_index += 1
            print('mark5')
            print('<<<End calculation for timestep, Case 1 or 5>>>')
            continue
        
        # STEP 4
        # ------ 
        else:
            print('mark6')
            if float(phi_HC_nd_un) > 0:
                phi_HC_nd_ac = phi_H_max
                print('mark7')
            elif float(phi_HC_nd_un) < 0:
                phi_HC_nd_ac = phi_C_max
                print('mark8')
        # Other combined heat conductances
        H_tr_2 = H_tr_1 + H_tr_w
        H_tr_3 = 1 / (1/H_tr_2 + 1/H_tr_ms)
        # Set theta_m_tp as theta_m_t from previous step
        if current_index == 0:
            theta_m_tp = 0
            theta_m_t = 0
        else:
            theta_m_tp = theta_m_t
        phi_HC_nd = phi_HC_nd_ac    
        phi_mtot = phi_m + H_tr_em * theta_sup + H_tr_3 * (phi_st + H_tr_w * theta_sup + H_tr_1 * (((phi_ia + phi_HC_nd)/H_ve_adj) + theta_sup)) / H_tr_2
        theta_m_tp = theta_m_tp_list[0] #EJW mtp
        df.theta_m_t[current_index] = (theta_m_tp * ((C_m/3600) - 0.5 * (H_tr_3 + H_tr_em)) + phi_mtot) / ((C_m/3600) + 0.5 * (H_tr_3 + H_tr_em))
        theta_m_t = df.theta_m_t[current_index]
        theta_m_tp_list.clear() #EJW mtp
        theta_m_tp_list.append(theta_m_t) #EJW mtp
        theta_m = (theta_m_t + theta_m_tp)/2 
        theta_s = (H_tr_ms * theta_m + phi_st + H_tr_w * theta_sup + H_tr_1 * (theta_sup + (phi_ia + phi_HC_nd)/H_ve_adj)) / (H_tr_ms + H_tr_w + H_tr_1)
        df.theta_air_ac[current_index] = (H_tr_is * theta_s + H_ve_adj * theta_sup + phi_ia + phi_HC_nd) / (H_tr_is + H_ve_adj)
        theta_air_ac = float(df.theta_air_ac[current_index])
        df.theta_air[current_index] = df.theta_air_ac[current_index]
        theta_op = 0.3 * theta_air_ac + 0.7 * theta_s
        # The energy need (kW) for heating or cooling for a given hour, Q_HC_nd, is positive in the case of heating need and negative in the case of cooling need
        df.Q_HC_nd[current_index] = phi_HC_nd_ac / 1000
        # Heating
        df.Q_H_nd[current_index] = max(0, float(df.Q_HC_nd[current_index])) 
        # Cooling
        df.Q_C_nd[current_index] = abs(min(0, float(df.Q_HC_nd[current_index]))) 
        
        # Other (EJW: also add to unrestricted if statement)
        # Internal and solar heat gains (MJ)
        Q_int = phi_int * 0.036
        Q_sol = phi_sol * 0.036

        print('<<<End calculation for timestep, Case 2 or 4>>>')

        current_timestamp += delta
        current_index += 1
        
    print('LOADING RESULTS')
    # Results
    #results = {'Date': df.index.strftime('%d/%m %H:%M:%S'), 'Hour of day':df.hour_of_day,'Day of week':df.day_of_week,'Outside temperature (DegC)':df.t_outside_t2m_degC,'Actual internal temperature (DegC)':df.theta_air,'Heating demand':df.Q_H_nd,'Cooling demand':df.Q_C_nd,'phi_int':df.phi_int,'phi_sol':df.phi_sol,'i_sol':df.i_sol,'theta_air_0':df.theta_air_0,'theta_air_10':df.theta_air_10,'theta_m_tp':df.theta_m_tp, 'theta_m_t':df.theta_m_t}
    #df_results = pd.DataFrame(results)
    #df_results.to_csv('Output/output'+'_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    #daymonthtime = df.index.time().strftime('%H:%M:%S')
    results_lite = {'Date':df.dmt,'SH':df.Q_H_nd,'SC':df.Q_C_nd}
    df_results = pd.DataFrame(results_lite)
    #df_results.to_csv('Output/output'+'_'+time.strftime("%Y%m%d-%H%M%S")+'.csv')
    
    ret = dict()
    ret["graphs"] = {}
    ret["graphs"]["Space Heating Demand"] = {}
    ret["graphs"]["Space Heating Demand"]["type"] = "line"
    ret["graphs"]["Space Heating Demand"]["values"] = df_results["SH"]
    ret["graphs"]["Space Heating Demand"]["values"] = df_results["SC"]

    ret["values"] = {
        "Total space heating demand (kW)": sum(df_results["SH"])
        }
    
    #validate(ret)
    return ret
    
'''
test = buildingload(
            geojson=gj,
            building_type="SFH",
            construction_year=2020,
            gfa_external=100.0,
            n_stories=1,
            t_set_min=20.0,
            t_set_max=26.0,
            user_month="January",
            user_week="Week 1",
            user_day="Monday",
            user_model_length="Day",
            roof_type_orientation="0",
            user_roof_pitch=30.0,
            w_f_r=1.3,
            L=1,
            W=1,
            facade_orientation="north",
            a_door=2.0,
            window_front_proportion=10.0,
            window_back_proportion=25.0,
            window_side_1_proportion=25.0,
            window_side_2_proportion=25.0
        )
print(test)
'''