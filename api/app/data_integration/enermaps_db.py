#!/usr/bin/python
from configparser import ConfigParser
import psycopg2
from app.common import db


# def connect():
#     print("Database connection...")
#     try:
#         db_con = db.get_db()
#     except Exception:
#         if db_con is not None:
#             db_con.close()
#         raise
#     return db_con.cursor()

def connect():
    """ Connect to the PostgreSQL database server """
    try:
        params = {
            "host" : "0.0.0.0",
            "database" : "dataset",
            "user" : "mel",
            "password" : "mel",
            "port" : 5432
        }
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params, options='-c statement_timeout=300000')
        return  conn
    except Exception  as error:
        print("Error while connecting to PostgreSQL", error)
        raise


def get_datasets_ids():
    """
    Get the ids of all datasets in the database 
    """
    cursor = connect()
    try:
        cursor.execute(
                """
                SELECT ds_id FROM datasets 
                ORDER BY ds_id;
                """
            )
        datasets = cursor.fetchall()
        return datasets
    except psycopg2.Error as e:
        print("SQL error in get_datasets_ids")
        print(e)
        raise
    except Exception as e:
        print("Other exception in get_datasets_ids")
        print(e)
    finally:
        cursor.close()


def get_dataset_name(cursor, dataset_id):
    """
    Return the human readable name of a dataset.
    """
    SQL = (
                """
                 SELECT ds_id, metadata ->> 'Title (with Hyperlink)' as "Name" FROM datasets 
                 ORDER BY ds_id;
                """
           )
    data = dataset_id
    try:
        cursor.execute(SQL, data)
        datasets = cursor.fetchall()
        return datasets
        #return [dataset for dataset in datasets]
    except psycopg2.Error as e:
        print("SQL error in get_datasets_names")
        print(e)
        raise


# def get_datasets_names(cursor):
#     """
#     Return a tuple (dataset_id, dataset_human_readable_name)
#     """
#     try:
#         cursor.execute(
#                 """
#                 SELECT ds_id, metadata ->> 'Title (with Hyperlink)' as "Name" FROM datasets 
#                 ORDER BY ds_id;
#                 """
#             )
#         datasets = cursor.fetchall()
#         return [dataset for dataset in datasets]
#     except psycopg2.Error as e:
#         print("SQL error in get_datasets_names")
#         print(e)
#         raise


def dataset_query(cursor, dataset_id):
    """
    THIS FUNCTION CANNOT BE USED WITHOUT PARAMETERS ON ALL DATASETS
    (TAKES TOO MUCH TIME)
    """
    SQL = (
            """
            SELECT data.fid,
                    json_object_agg(variable, value),
                    fields,
                    start_at, dt, z, data.ds_id, metadata, geometry FROM data
            INNER JOIN spatial ON data.fid = spatial.fid
            INNER JOIN datasets ON data.ds_id = datasets.ds_id
            WHERE data.ds_id = %s
            GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry, metadata
            ORDER BY data.fid;
            """
        )
    data = dataset_id
    try:
        cursor.execute(SQL, data)
    except psycopg2.OperationalError as e:
        print("SQL operational error in dataset_query")
        print(e)
        raise
    except psycopg2.Error as e:
        print("Other SQL error in dataset_query")
        print(e)
        raise 


def get_dataset_metadata(cursor, dataset_id):
    """
    Get the metadata for one dataset
    """
    SQL = (
        """
        SELECT (metadata ->> 'variables')::jsonb as variables,
                metadata ->> 'start_at' as start_at ,
                TO_TIMESTAMP(metadata ->> 'end_at', 'YYYY-MM-DD HH24:MI')::timestamp without time zone as end_at,
                (metadata ->> 'parameters')::jsonb as parameters,
                (metadata ->> 'is_raster')::bool as is_raster,
                metadata ->> 'temporal_granularity' as temporal_granularity,
                (metadata ->> 'custom_periods')::jsonb as custom_periods,
                (metadata ->> 'is_tiled')::bool as is_tiled,
                (metadata ->> 'levels')::jsonb as levels,
                (metadata ->>' to_be_fixed')::bool as to_be_fixed from datasets
        WHERE ds_id = %s;
        """
        )
    data = (dataset_id,)
    try:
        cursor.execute(SQL, data)
    except psycopg2.OperationalError as e:
        print("SQL error in get_dataset_metadata")
        print(e)
        raise
    except psycopg2.Error as e:
        print("Other SQL exception in get_dataset_metadata")
        print(e)
        raise 


def get_default_datastet_query_parameters(curs, dataset_id):

    variables = None
    # start_at = None
    end_at = None
    parameters = None
    is_raster = None
    # temporal_granularity = None
    # custom_periods = None
    is_tiled = None
    levels = None
    to_be_fixed = None

    try:
        # This should be only one line of the metadata table
        get_dataset_metadata(curs, dataset_id)
        res = curs.fetchone()
        #TODO check that there is only one line returned
    except psycopg2.Error:
        raise

    try:
        variables = res[0] 
        # start_at = res[1]
        end_at = res[2]
        parameters = res[3]
        is_raster = res[4]
        # temporal_granularity = res[5]
        # custom_periods = res[6]
        is_tiled = res[7]
        levels = res[8]
        to_be_fixed = res[9]
    except IndexError:
        print("Index error")
        raise

    # The dataset still has an error in its data/metadata?
    if to_be_fixed:
        print("TO BE FIXED")
        raise Exception
        
    # Construct the query string -------------------------------------------    
    default_dataset_query_params = ""

    s_1 = """"data.ds_id": {dataset_id}""".format(dataset_id=dataset_id)

    # Take the newest dataset
    s_2 = None 
    if end_at:
        dataset_date = end_at
        s_2 = """"start_at": "'{start_at}'" """.format(start_at=dataset_date)

    s_3 = None
    if levels:
        level = levels[0]
        s_3 = """"level": "{""" + """{level}""".format(level=level) + """}\""""

    # "variables" are only for raster type, if vector type "variables" are something to be
    # printed next to the geometries
    s_4 = None
    if variables and is_raster:
        variable = variables[0]
        s_4 = """"variable": "'{variable}'" """.format(variable=variable)

    s_5 = None
    dataset_params = []
    if parameters:
        l = len(list(parameters))
        p = ""
        for i, k in enumerate(parameters):
            dataset_params.append(parameters[k][0])
            if i < (l - 1):
                p += """ "{k}" : """.format(k=k) + "\"" + parameters[k][0] + "\", " 
            else:
                p += """ "{k}" : """.format(k=k) + "\"" + parameters[k][0] + "\"" 
        s_5 = """ "fields" : {""" +   """{p}""".format(p=p) + "}"

    if is_raster:
        # print("is raster")
        if is_tiled:
            # print("is tiled")
            if s_2 is not None:
                if s_3 is not None:
                    if s_5 is not None:
                        default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 + ", " + s_5 + "}"
                    else:
                        default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 + "}"
                else:
                    if s_5 is not None:
                        default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_5 + "}"
                    else:
                        default_dataset_query_params = "{" + s_1 + ", " + s_2 + "}"
            else:
                if s_3 is not None:
                    if s_5 is not None:
                        default_dataset_query_params = "{" + s_1 + ", " + s_3 + ", " + s_5 + "}"
                    else:
                        default_dataset_query_params = "{" + s_1 + ", " + s_3 + "}"
                else:
                    if s_5 is not None:
                        default_dataset_query_params = "{" + s_1 + ", " + s_5 + "}"
                    else:
                        default_dataset_query_params = "{" + s_1 + """ , "intersecting":"POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))" """ + "}"
        else:
            # print("is not tiled")
            if s_2 is not None:
                if s_3 is not None:
                    if s_4 is not None:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 + ", " + s_4 +  ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 + ", " + s_4 + "}"
                    else:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 +  ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 + "}"
                else:
                    if s_4 is not None:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_4 +  ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_4 + "}"
                    else:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 +  ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_2 + "}"
            else:
                if s_3 is not None:
                    if s_4 is not None:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_3 + ", " + s_4 + ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_3 + ", " + s_4 + "}"
                    else:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_3 +  ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_3 + "}"
                else:
                    if s_4 is not None:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 + ", " + s_4 +  ", " + s_5 +  "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + ", " + s_4 + "}"
                    else:
                        if s_5 is not None:
                            default_dataset_query_params = "{" + s_1 +  ", " + s_5 + "}"
                        else:
                            default_dataset_query_params = "{" + s_1 + "}"
    else:
        # print("is vector")
        if s_2 is not None:
            if s_3 is not None:
                
                if s_5 is not None:
                    default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 +  ", " + s_5 + "}"
                else:
                    default_dataset_query_params = "{" + s_1 + ", " + s_2 + ", " + s_3 + "}"
            else:
                if s_5 is not None:
                    default_dataset_query_params = "{" + s_1 + ", " + s_2 +  ", " + s_5 + "}"
                else:
                    default_dataset_query_params = "{" + s_1 + ", " + s_2 + "}"
        else:
            if s_3 is not None:
                if s_5 is not None:
                    default_dataset_query_params = "{" + s_1 + ", " + s_3 + ", " + s_5 + "}"
                else:
                    default_dataset_query_params = "{" + s_1 + ", " + s_3 + "}"
            else:
                if s_5 is not None:
                    default_dataset_query_params = "{" + s_1 + ", " + s_5 + "}"
                else:
                    default_dataset_query_params = "{" + s_1 + "}"
            
    return default_dataset_query_params