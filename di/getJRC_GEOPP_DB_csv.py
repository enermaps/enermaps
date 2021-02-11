from dataflows import Flow, load, dump_to_path, dump_to_zip, printer, add_metadata, update_package, update_resource, update_schema, set_primary_key
from dataflows import sort_rows, filter_rows, find_replace, delete_fields, select_fields
from dataflows import add_computed_field, unpivot, set_type, validate, unpivot 
from datapackage import Package
import json

unpivoting_fields = [
    { 'name': '^(?!latitude$)(?!longitude$)(?!extra_fields$)([a-z0-9!@#$&()-`.+,/\"]+$)', #all fields, but lat, long and extra
    'keys': {'variable': r'\1'} }
]

extra_keys = [ {'name': 'variable', 'type': 'string'}]

extra_value = {'name': 'value', 'type': 'number'}

selected_fields = ["id_powerplant",'gross_cap_ele','ini_cap_ele', 'gross_cap_th', 'extra_fields', 'latitude', 'longitude']

url = 'http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/JRCOD/RES-DATA/10001/LATEST/JRC-GEOPP-DB.csv'


def add_extras_to_schema(package):
    # Add a new field to the first resource
    package.pkg.descriptor["resources"][0]["schema"]["fields"].append(
        dict(name="extra_fields", type="object")
    )
    # Must yield the modified datapackage
    yield package.pkg
    # And its resources
    yield from package


def add_extras_column(row):
    extra_fields = {}
    for key,value in row.items():
        if key not in selected_fields:
            extra_fields[key] = value
    row["extra_fields"] = json.dumps(extra_fields)


def retrieve(*args):
    return Flow(
        # Load inputs
        load(url, format='csv', ),
        
        # Process them (if necessary)
        update_package(name="jrc_geopp_db_csv"),
        update_resource('JRC-GEOPP-DB', name='jrc_geopp_db', path='jrc_geopp_db.csv'),
        add_extras_to_schema,
        add_extras_column,
        # printer(),
        select_fields(selected_fields, resources=None),
        printer(),
        unpivot(unpivoting_fields, extra_keys, extra_value, regex=True),
        add_computed_field(target=dict(name='Location', type='geopoint'), operation='format', with_='{longitude}, {latitude}'),
        delete_fields(['latitude', 'longitude']),
        
        # # Update metadata
        set_primary_key('id_powerplant'),
        update_package(sources = [{
                                    "title": "Joint Research Centre Data Catalogue",
                                    "path": "https://data.jrc.ec.europa.eu/dataset/jrc-10128-10001"
                                }]),
        # printer(),
        find_replace([{"name": "value", "patterns":[{"find":"NULL","replace":""}]}], resources=None),
        # update_resource(None,path=url),
        update_schema(None, missingValues=["NULL", ""]),
        set_type('value',type="number"),
        validate()

        # printer(),
    )



if __name__ == '__main__':
    Flow(retrieve(),
        dump_to_path(out_path='data/jrc_geopp_db',force_format=True,format="csv")
        ).process(),
        # printer()).process()