from dataflows import Flow, load, dump_to_path, dump_to_zip, printer, add_metadata, update_package, update_resource, update_schema, set_primary_key
from dataflows import sort_rows, filter_rows, find_replace, delete_fields, select_fields
from dataflows import add_computed_field, unpivot, set_type, validate, unpivot, duplicate, dump_to_sql
from datapackage import Package
import json

unpivoting_fields = [
    { 'name': '^(?!geometry$)(?!fields$)(?!FID$)([a-z0-9!@#$&()-`.+,/\"]+$)', #all fields, but lat, long and extra
    'keys': {'variable': r'\1'} }
]

extra_keys = [ {'name': 'variable', 'type': 'string'}]

extra_value = {'name': 'value', 'type': 'number'}

selected_fields = ['gross_cap_ele','ini_cap_ele', 'gross_cap_th', 'fields', 'latitude', 'longitude']
selected_fields.append("FID")
selected_fields_spatial = selected_fields.copy()
selected_fields_spatial.remove("FID")


url = 'http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/JRCOD/RES-DATA/10001/LATEST/JRC-GEOPP-DB.csv'


def add_extras_to_schema(package):
    # Add a new field to the first resource
    package.pkg.descriptor["resources"][0]["schema"]["fields"].append(
        dict(name="fields", type="object")
    )
    # Must yield the modified datapackage
    yield package.pkg
    # And its resources
    yield from package


def addFID(package):
    # Add a new field to the first resource
    package.pkg.descriptor["resources"][0]["schema"]["fields"].append(
        dict(name="FID", type="string")
    )
    # Must yield the modified datapackage
    yield package.pkg
    # And its resources
    yield from package
    
def fillFID(row):
    row["FID"] = "jrc_geopp_db-"+row["id_powerplant"]

def add_extras_column(row):
    extra_fields = {}
    for key,value in row.items():
        if key not in selected_fields:
            extra_fields[key] = value
    row["fields"] = json.dumps(extra_fields)


def retrieve(*args):
    return Flow(
        # Load inputs
        load(url, format='csv', ),
        
        # Process them (if necessary)
        update_package(name="jrc_geopp_db_csv"),
        update_resource('JRC-GEOPP-DB', name='jrc_geopp_db', path='jrc_geopp_db.csv'),
        add_extras_to_schema,
        add_extras_column,
        addFID,
        fillFID,
        # printer(num_rows=10),
        select_fields(selected_fields, resources=None),
        # printer(),
        # add_computed_field(target=dict(name='geometry', type='geopoint'), operation='format', with_='{longitude}, {latitude}'),
        add_computed_field(target=dict(name='geometry', type='string'), operation='format', with_='POINT({longitude} {latitude})'),
        delete_fields(['latitude', 'longitude']),
        
        # # Update metadata
        set_primary_key('id_powerplant'),
        update_package(sources = [{
                                    "title": "Joint Research Centre Data Catalogue",
                                    "path": "https://data.jrc.ec.europa.eu/dataset/jrc-10128-10001"
                                }]),
        # printer(),
        # Resource 1
        duplicate(source="jrc_geopp_db", target_name="jrc_geopp_db_spatial", target_path="jrc_geopp_db_spatial.csv"),
        delete_fields(selected_fields_spatial,resources=1),
        # printer(num_rows=10),

        # Resource 0
        unpivot(unpivoting_fields, extra_keys, extra_value, regex=True,  resources=0),
        delete_fields(['geometry'],resources=0),
        find_replace([{"name": "value", "patterns":[{"find":"NULL","replace":""}]}], resources=0),
        # update_schema(None, missingValues=["NULL", ""], resources=0),
        set_type('value',type="number", resources=0),
        # validate()
        # printer(num_rows=10),
    )



if __name__ == '__main__':
    host = "enermaps_db_1"
    port = 5432
    ds_id = 2
    # host = "localhost"
    # port = 5433
    Flow(retrieve(),
        dump_to_path(out_path='data/jrc_geopp_db',format="csv")
        # dump_to_sql({"spatial":{"resource-name":"jrc_geopp_db_spatial", "mode":"append"},
        #             "data":{"resource-name":"jrc_geopp_db", "mode":"append"}},
        #             engine="postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port))
        ).process()
    
    import pandas as pd
    import geopandas as gpd
    import utilities
    from shapely import wkt
    import shutil
    datasets = pd.read_csv("datasets.csv",engine="python",index_col=[0])
    dataset = pd.DataFrame([{"ds_id": ds_id, "metadata":datasets.loc[ds_id].to_json()}])
    utilities.toPostgreSQL(dataset,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="datasets")
    
    data = pd.read_csv("data/jrc_geopp_db/jrc_geopp_db.csv")
    data["ds_id"] =  ds_id
    utilities.toPostgreSQL(data,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="data")

    
    spatial = pd.read_csv("data/jrc_geopp_db/jrc_geopp_db_spatial.csv")
    spatial['geometry'] = spatial['geometry'].apply(wkt.loads)
    spatial = gpd.GeoDataFrame(spatial)
    spatial.crs = "EPSG:4326"
    spatial = spatial.to_crs("EPSG:3035")
    spatial["ds_id"] =  ds_id
    utilities.toPostGIS(spatial,"postgresql://test:example@{host}:{port}/dataset".format(host=host,port=port), schema="spatial")
    
    shutil.rmtree("data/jrc_geopp_db/")
    
    