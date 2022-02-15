import os
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.ops import nearest_points
from joblib import Parallel, delayed


nr_cores = 10


def split_shape(gdf, country_path_dict):
    for key in country_path_dict.keys():
        print(key)
        tmp_gdf = gdf[gdf.CNTR_CODE == key].copy()
        tmp_gdf.to_file(country_path_dict[key]['lau2'])
        tmp_gdf = None
    print('Split shape done!')


def overlay_light(lau2, shapefile, output):
    gdf1 = gpd.read_file(lau2)
    gdf2 = gpd.read_file(shapefile)
    geoms = [item.centroid for item in gdf2.geometry]
    gdf2.geometry = geoms
    join = gpd.sjoin(gdf2, gdf1, how='right').loc[:, ['dhPot_2020', 'dhPot_2050', 'GISCO_ID', 'geometry']]
    join = join.dissolve(by='GISCO_ID', aggfunc='sum', as_index=False, dropna=True)
    join = join[join.dhPot_2050 > 0].copy()
    join.to_file(output)
    gdf1 = gdf2 = geoms = join = None

def copy_for_isi(src, dst):
    import shutil
    shutil.copytree(src, dst)


if __name__ == "__main__":
    input_directory = '/media/SSD3.5TB/workspace_mostafa/mostafa_projects/data_warehouse/lau2019'
    output_directory = '/media/SSD3.5TB/workspace_mostafa/mostafa_projects/outputs/res_hc_pathways'
    lau2 = os.path.join(input_directory, "LAU_RG_01M_2019_3035.shp")
    #gdf = gpd.read_file(lau2)
    skiped_countries = []
    country_path_dict = dict()
    for directory, foldernames, filenames in os.walk(output_directory):
        # find the right directory
        flag = False
        for fname in filenames:
            if "Energy_TOTAL_" in fname:
                flag = True
        if flag == False:
            continue
        country = directory.split("/")[-2][-2::]
        if len(foldernames) != 1:
            skiped_countries.append(country)
            continue
        scenario = foldernames[0]

        '''if country != 'AT':
            continue'''
        country_path_dict[country] = {
            'lau2': os.path.join(directory, '%s_lau2.shp' % country),
            'shp2': os.path.join(directory, '%s/shape2.shp' % scenario),
            'shp3': os.path.join(directory, '%s/overlay.shp' % scenario)
        }
    #split_shape(gdf, country_path_dict)
    gdf = None
    '''
    for key in country_path_dict.keys():
        print(key)
        overlay_light(country_path_dict[key]['lau2'], country_path_dict[key]['shp2'],
                               country_path_dict[key]['shp3'])
    '''
    # parallel computing
    Parallel(n_jobs=nr_cores)(
        delayed(overlay_light)(country_path_dict[key]['lau2'], country_path_dict[key]['shp2'],
                               country_path_dict[key]['shp3']) for key in country_path_dict.keys())

    print(skiped_countries)
