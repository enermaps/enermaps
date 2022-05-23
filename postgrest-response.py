postgrest_rep = {
    "swagger": "2.0",
    "info": {
        "version": "7.0.1 (UNKNOWN)",
        "title": "PostgREST API",
        "description": "standard public schema",
    },
    "host": "0.0.0.0:3000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json", "application/vnd.pgrst.object+json", "text/csv"],
    "produces": ["application/json", "application/vnd.pgrst.object+json", "text/csv"],
    "paths": {
        "/": {
            "get": {
                "tags": ["Introspection"],
                "summary": "OpenAPI description (this document)",
                "produces": ["application/openapi+json", "application/json"],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/datacite": {
            "get": {
                "tags": ["datacite"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.datacite.data"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/datacite"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            }
        },
        "/dataset_list": {
            "get": {
                "tags": ["dataset_list"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.dataset_list.ds_id"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.title"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.is_raster"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.is_tiled"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.shared_id"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.group"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/dataset_list"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            },
            "post": {
                "tags": ["dataset_list"],
                "parameters": [
                    {"$ref": "#/parameters/body.dataset_list"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"201": {"description": "Created"}},
            },
            "delete": {
                "tags": ["dataset_list"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.dataset_list.ds_id"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.title"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.is_raster"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.is_tiled"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.shared_id"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.group"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
            "patch": {
                "tags": ["dataset_list"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.dataset_list.ds_id"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.title"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.is_raster"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.is_tiled"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.shared_id"},
                    {"$ref": "#/parameters/rowFilter.dataset_list.group"},
                    {"$ref": "#/parameters/body.dataset_list"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
        },
        "/datasets": {
            "get": {
                "tags": ["datasets"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.datasets.ds_id"},
                    {"$ref": "#/parameters/rowFilter.datasets.metadata"},
                    {"$ref": "#/parameters/rowFilter.datasets.shared_id"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/datasets"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            },
            "post": {
                "tags": ["datasets"],
                "parameters": [
                    {"$ref": "#/parameters/body.datasets"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"201": {"description": "Created"}},
            },
            "delete": {
                "tags": ["datasets"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.datasets.ds_id"},
                    {"$ref": "#/parameters/rowFilter.datasets.metadata"},
                    {"$ref": "#/parameters/rowFilter.datasets.shared_id"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
            "patch": {
                "tags": ["datasets"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.datasets.ds_id"},
                    {"$ref": "#/parameters/rowFilter.datasets.metadata"},
                    {"$ref": "#/parameters/rowFilter.datasets.shared_id"},
                    {"$ref": "#/parameters/body.datasets"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
        },
        "/geography_columns": {
            "get": {
                "tags": ["geography_columns"],
                "parameters": [
                    {
                        "$ref": "#/parameters/rowFilter.geography_columns.f_table_catalog"
                    },
                    {"$ref": "#/parameters/rowFilter.geography_columns.f_table_schema"},
                    {"$ref": "#/parameters/rowFilter.geography_columns.f_table_name"},
                    {
                        "$ref": "#/parameters/rowFilter.geography_columns.f_geography_column"
                    },
                    {
                        "$ref": "#/parameters/rowFilter.geography_columns.coord_dimension"
                    },
                    {"$ref": "#/parameters/rowFilter.geography_columns.srid"},
                    {"$ref": "#/parameters/rowFilter.geography_columns.type"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/geography_columns"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            }
        },
        "/geometry_columns": {
            "get": {
                "tags": ["geometry_columns"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_catalog"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_schema"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_name"},
                    {
                        "$ref": "#/parameters/rowFilter.geometry_columns.f_geometry_column"
                    },
                    {"$ref": "#/parameters/rowFilter.geometry_columns.coord_dimension"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.srid"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.type"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/geometry_columns"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            },
            "post": {
                "tags": ["geometry_columns"],
                "parameters": [
                    {"$ref": "#/parameters/body.geometry_columns"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"201": {"description": "Created"}},
            },
            "delete": {
                "tags": ["geometry_columns"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_catalog"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_schema"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_name"},
                    {
                        "$ref": "#/parameters/rowFilter.geometry_columns.f_geometry_column"
                    },
                    {"$ref": "#/parameters/rowFilter.geometry_columns.coord_dimension"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.srid"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.type"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
            "patch": {
                "tags": ["geometry_columns"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_catalog"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_schema"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.f_table_name"},
                    {
                        "$ref": "#/parameters/rowFilter.geometry_columns.f_geometry_column"
                    },
                    {"$ref": "#/parameters/rowFilter.geometry_columns.coord_dimension"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.srid"},
                    {"$ref": "#/parameters/rowFilter.geometry_columns.type"},
                    {"$ref": "#/parameters/body.geometry_columns"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
        },
        "/metadata": {
            "get": {
                "tags": ["metadata"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.metadata.ds_id"},
                    {"$ref": "#/parameters/rowFilter.metadata.shared_id"},
                    {"$ref": "#/parameters/rowFilter.metadata.metadata"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/metadata"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            }
        },
        "/parameters": {
            "get": {
                "tags": ["parameters"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.parameters.ds_id"},
                    {"$ref": "#/parameters/rowFilter.parameters.title"},
                    {"$ref": "#/parameters/rowFilter.parameters.variables"},
                    {"$ref": "#/parameters/rowFilter.parameters.start_at"},
                    {"$ref": "#/parameters/rowFilter.parameters.end_at"},
                    {"$ref": "#/parameters/rowFilter.parameters.fields"},
                    {"$ref": "#/parameters/rowFilter.parameters.is_raster"},
                    {"$ref": "#/parameters/rowFilter.parameters.temporal_granularity"},
                    {"$ref": "#/parameters/rowFilter.parameters.time_periods"},
                    {"$ref": "#/parameters/rowFilter.parameters.is_tiled"},
                    {"$ref": "#/parameters/rowFilter.parameters.levels"},
                    {"$ref": "#/parameters/rowFilter.parameters.default_parameters"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/parameters"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            },
            "post": {
                "tags": ["parameters"],
                "parameters": [
                    {"$ref": "#/parameters/body.parameters"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"201": {"description": "Created"}},
            },
            "delete": {
                "tags": ["parameters"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.parameters.ds_id"},
                    {"$ref": "#/parameters/rowFilter.parameters.title"},
                    {"$ref": "#/parameters/rowFilter.parameters.variables"},
                    {"$ref": "#/parameters/rowFilter.parameters.start_at"},
                    {"$ref": "#/parameters/rowFilter.parameters.end_at"},
                    {"$ref": "#/parameters/rowFilter.parameters.fields"},
                    {"$ref": "#/parameters/rowFilter.parameters.is_raster"},
                    {"$ref": "#/parameters/rowFilter.parameters.temporal_granularity"},
                    {"$ref": "#/parameters/rowFilter.parameters.time_periods"},
                    {"$ref": "#/parameters/rowFilter.parameters.is_tiled"},
                    {"$ref": "#/parameters/rowFilter.parameters.levels"},
                    {"$ref": "#/parameters/rowFilter.parameters.default_parameters"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
            "patch": {
                "tags": ["parameters"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.parameters.ds_id"},
                    {"$ref": "#/parameters/rowFilter.parameters.title"},
                    {"$ref": "#/parameters/rowFilter.parameters.variables"},
                    {"$ref": "#/parameters/rowFilter.parameters.start_at"},
                    {"$ref": "#/parameters/rowFilter.parameters.end_at"},
                    {"$ref": "#/parameters/rowFilter.parameters.fields"},
                    {"$ref": "#/parameters/rowFilter.parameters.is_raster"},
                    {"$ref": "#/parameters/rowFilter.parameters.temporal_granularity"},
                    {"$ref": "#/parameters/rowFilter.parameters.time_periods"},
                    {"$ref": "#/parameters/rowFilter.parameters.is_tiled"},
                    {"$ref": "#/parameters/rowFilter.parameters.levels"},
                    {"$ref": "#/parameters/rowFilter.parameters.default_parameters"},
                    {"$ref": "#/parameters/body.parameters"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
        },
        "/raster_columns": {
            "get": {
                "tags": ["raster_columns"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.raster_columns.r_table_catalog"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.r_table_schema"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.r_table_name"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.r_raster_column"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.srid"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.scale_x"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.scale_y"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.blocksize_x"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.blocksize_y"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.same_alignment"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.regular_blocking"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.num_bands"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.pixel_types"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.nodata_values"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.out_db"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.extent"},
                    {"$ref": "#/parameters/rowFilter.raster_columns.spatial_index"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/raster_columns"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            }
        },
        "/raster_overviews": {
            "get": {
                "tags": ["raster_overviews"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.raster_overviews.o_table_catalog"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.o_table_schema"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.o_table_name"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.o_raster_column"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.r_table_catalog"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.r_table_schema"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.r_table_name"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.r_raster_column"},
                    {"$ref": "#/parameters/rowFilter.raster_overviews.overview_factor"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/raster_overviews"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            }
        },
        "/spatial_ref_sys": {
            "get": {
                "tags": ["spatial_ref_sys"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.srid"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.auth_name"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.auth_srid"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.srtext"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.proj4text"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/order"},
                    {"$ref": "#/parameters/range"},
                    {"$ref": "#/parameters/rangeUnit"},
                    {"$ref": "#/parameters/offset"},
                    {"$ref": "#/parameters/limit"},
                    {"$ref": "#/parameters/preferCount"},
                ],
                "responses": {
                    "206": {"description": "Partial Content"},
                    "200": {
                        "schema": {
                            "items": {"$ref": "#/definitions/spatial_ref_sys"},
                            "type": "array",
                        },
                        "description": "OK",
                    },
                },
            },
            "post": {
                "tags": ["spatial_ref_sys"],
                "parameters": [
                    {"$ref": "#/parameters/body.spatial_ref_sys"},
                    {"$ref": "#/parameters/select"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"201": {"description": "Created"}},
            },
            "delete": {
                "tags": ["spatial_ref_sys"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.srid"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.auth_name"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.auth_srid"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.srtext"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.proj4text"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
            "patch": {
                "tags": ["spatial_ref_sys"],
                "parameters": [
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.srid"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.auth_name"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.auth_srid"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.srtext"},
                    {"$ref": "#/parameters/rowFilter.spatial_ref_sys.proj4text"},
                    {"$ref": "#/parameters/body.spatial_ref_sys"},
                    {"$ref": "#/parameters/preferReturn"},
                ],
                "responses": {"204": {"description": "No Content"}},
            },
        },
        "/rpc/pgis_geometry_accum_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_accum_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_metadata": {
            "post": {
                "tags": ["(rpc) st_metadata"],
                "summary": "args: rast - Returns basic meta data about a raster object such as pixel size, rotation (skew), upper, lower left, etc.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast - Returns basic meta data about a raster object such as pixel size, rotation (skew), upper, lower left, etc.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mapalgebraexpr": {
            "post": {
                "tags": ["(rpc) st_mapalgebraexpr"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "band1",
                                "rast2",
                                "band2",
                                "expression",
                            ],
                            "type": "object",
                            "properties": {
                                "nodata2expr": {"format": "text", "type": "string"},
                                "rast1": {"format": "raster", "type": "string"},
                                "band1": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "rast2": {"format": "raster", "type": "string"},
                                "nodata1expr": {"format": "text", "type": "string"},
                                "expression": {"format": "text", "type": "string"},
                                "band2": {"format": "integer", "type": "integer"},
                                "nodatanodataval": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "extenttype": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multipointfromwkb": {
            "post": {
                "tags": ["(rpc) st_multipointfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_line_interpolate_point": {
            "post": {
                "tags": ["(rpc) st_line_interpolate_point"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asx3d": {
            "post": {
                "tags": ["(rpc) st_asx3d"],
                "summary": "args: g1, maxdecimaldigits=15, options=0 - Returns a Geometry in X3D xml node element format: ISO-IEC-19776-1.2-X3DEncodings-XML",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: g1, maxdecimaldigits=15, options=0 - Returns a Geometry in X3D xml node element format: ISO-IEC-19776-1.2-X3DEncodings-XML",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "options": {"format": "integer", "type": "integer"},
                                "maxdecimaldigits": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asbinary": {
            "post": {
                "tags": ["(rpc) st_asbinary"],
                "summary": "args: rast, outasin=FALSE - Return the Well-Known Binary (WKB) representation of the raster without SRID meta data.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast, outasin=FALSE - Return the Well-Known Binary (WKB) representation of the raster without SRID meta data.",
                            "properties": {
                                "outasin": {"format": "boolean", "type": "boolean"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_setvalues": {
            "post": {
                "tags": ["(rpc) _st_setvalues"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "x", "y", "newvalueset"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "keepnodata": {"format": "boolean", "type": "boolean"},
                                "newvalueset": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "nosetvalue": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "hasnosetvalue": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "x": {"format": "integer", "type": "integer"},
                                "noset": {"format": "boolean[]", "type": "string"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_intersection": {
            "post": {
                "tags": ["(rpc) st_intersection"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "band1",
                                "rast2",
                                "band2",
                                "returnband",
                                "nodataval",
                            ],
                            "type": "object",
                            "properties": {
                                "nodataval": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rast1": {"format": "raster", "type": "string"},
                                "band1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                                "band2": {"format": "integer", "type": "integer"},
                                "returnband": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force_3d": {
            "post": {
                "tags": ["(rpc) st_force_3d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gserialized_gist_joinsel_2d": {
            "post": {
                "tags": ["(rpc) gserialized_gist_joinsel_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_recv": {
            "post": {
                "tags": ["(rpc) geography_recv"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_m": {
            "post": {
                "tags": ["(rpc) st_m"],
                "summary": "args: a_point - Return the M coordinate of the point, or NULL if not available. Input must be a point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_point - Return the M coordinate of the point, or NULL if not available. Input must be a point.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force4d": {
            "post": {
                "tags": ["(rpc) st_force4d"],
                "summary": "args: geomA - Force the geometries into XYZM mode.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Force the geometries into XYZM mode.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromewkb": {
            "post": {
                "tags": ["(rpc) st_geomfromewkb"],
                "summary": "args: EWKB - Return a specified ST_Geometry value from Extended Well-Known Binary representation (EWKB).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: EWKB - Return a specified ST_Geometry value from Extended Well-Known Binary representation (EWKB).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_typmod_dims": {
            "post": {
                "tags": ["(rpc) postgis_typmod_dims"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_decompress_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_decompress_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/dropgeometrycolumn": {
            "post": {
                "tags": ["(rpc) dropgeometrycolumn"],
                "summary": "args: catalog_name, schema_name, table_name, column_name - Removes a geometry column from a spatial table.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "catalog_name",
                                "schema_name",
                                "table_name",
                                "column_name",
                            ],
                            "type": "object",
                            "description": "args: catalog_name, schema_name, table_name, column_name - Removes a geometry column from a spatial table.",
                            "properties": {
                                "catalog_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "table_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "column_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "schema_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_length_spheroid": {
            "post": {
                "tags": ["(rpc) st_length_spheroid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/dropgeometrytable": {
            "post": {
                "tags": ["(rpc) dropgeometrytable"],
                "summary": "args: catalog_name, schema_name, table_name - Drops a table and all its references in geometry_columns.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["catalog_name", "schema_name", "table_name"],
                            "type": "object",
                            "description": "args: catalog_name, schema_name, table_name - Drops a table and all its references in geometry_columns.",
                            "properties": {
                                "catalog_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "table_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "schema_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_overabove": {
            "post": {
                "tags": ["(rpc) raster_overabove"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_within": {
            "post": {
                "tags": ["(rpc) st_within"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastA lie in the exterior of raster rastB and at least one point of the interior of rastA lies in the interior of rastB.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastA lie in the exterior of raster rastB and at least one point of the interior of rastA lies in the interior of rastB.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_ge": {
            "post": {
                "tags": ["(rpc) geography_ge"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_distance_centroid": {
            "post": {
                "tags": ["(rpc) geometry_distance_centroid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pointfromgeohash": {
            "post": {
                "tags": ["(rpc) st_pointfromgeohash"],
                "summary": "args: geohash, precision=full_precision_of_geohash - Return a point from a GeoHash string.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geohash, precision=full_precision_of_geohash - Return a point from a GeoHash string.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_overlaps": {
            "post": {
                "tags": ["(rpc) geometry_overlaps"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isvaliddetail": {
            "post": {
                "tags": ["(rpc) st_isvaliddetail"],
                "summary": "args: geom, flags - Returns a valid_detail (valid,reason,location) row stating if a geometry is valid or not and if not valid, a reason why and a location where.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom, flags - Returns a valid_detail (valid,reason,location) row stating if a geometry is valid or not and if not valid, a reason why and a location where.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geomfromewkb": {
            "post": {
                "tags": ["(rpc) geomfromewkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_pixel_types": {
            "post": {
                "tags": ["(rpc) _raster_constraint_pixel_types"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distancespheroid": {
            "post": {
                "tags": ["(rpc) st_distancespheroid"],
                "summary": "args: geomlonlatA, geomlonlatB, measurement_spheroid - Returns the minimum distance between two lon/lat geometries given a particular spheroid. PostGIS versions prior to 1.5 only support points.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: geomlonlatA, geomlonlatB, measurement_spheroid - Returns the minimum distance between two lon/lat geometries given a particular spheroid. PostGIS versions prior to 1.5 only support points.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distance_sphere": {
            "post": {
                "tags": ["(rpc) st_distance_sphere"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_boundingdiagonal": {
            "post": {
                "tags": ["(rpc) st_boundingdiagonal"],
                "summary": "args: geom, fits=false - Returns the diagonal of the supplied geometrys bounding box.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom, fits=false - Returns the diagonal of the supplied geometrys bounding box.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "fits": {"format": "boolean", "type": "boolean"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box": {
            "post": {
                "tags": ["(rpc) box"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_tpi": {
            "post": {
                "tags": ["(rpc) st_tpi"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "customextent"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "customextent": {"format": "raster", "type": "string"},
                                "interpolate_nodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box2df_in": {
            "post": {
                "tags": ["(rpc) box2df_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geom2d_brin_inclusion_add_value": {
            "post": {
                "tags": ["(rpc) geom2d_brin_inclusion_add_value"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_coverage_tile": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_coverage_tile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_project": {
            "post": {
                "tags": ["(rpc) st_project"],
                "summary": "args: g1, distance, azimuth - Returns a POINT projected from a start point using a distance in meters and bearing (azimuth) in radians.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geog", "distance", "azimuth"],
                            "type": "object",
                            "description": "args: g1, distance, azimuth - Returns a POINT projected from a start point using a distance in meters and bearing (azimuth) in radians.",
                            "properties": {
                                "geog": {"format": "geography", "type": "string"},
                                "distance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "azimuth": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_raster_scripts_installed": {
            "post": {
                "tags": ["(rpc) postgis_raster_scripts_installed"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_wkttosql": {
            "post": {
                "tags": ["(rpc) st_wkttosql"],
                "summary": "args: WKT - Return a specified ST_Geometry value from Well-Known Text representation (WKT). This is an alias name for ST_GeomFromText",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT - Return a specified ST_Geometry value from Well-Known Text representation (WKT). This is an alias name for ST_GeomFromText",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_memunion": {
            "post": {
                "tags": ["(rpc) st_memunion"],
                "summary": "args: geomfield - Same as ST_Union, only memory-friendly (uses less memory and more processor time).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomfield - Same as ST_Union, only memory-friendly (uses less memory and more processor time).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_overview_constraint": {
            "post": {
                "tags": ["(rpc) _overview_constraint"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "ov",
                                "factor",
                                "refschema",
                                "reftable",
                                "refcolumn",
                            ],
                            "type": "object",
                            "properties": {
                                "reftable": {"format": "name", "type": "string"},
                                "factor": {"format": "integer", "type": "integer"},
                                "ov": {"format": "raster", "type": "string"},
                                "refcolumn": {"format": "name", "type": "string"},
                                "refschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_expand": {
            "post": {
                "tags": ["(rpc) st_expand"],
                "summary": "args: geom, dx, dy, dz=0, dm=0 - Returns bounding box expanded in all directions from the bounding box of the input geometry. Uses double-precision",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "dx", "dy"],
                            "type": "object",
                            "description": "args: geom, dx, dy, dz=0, dm=0 - Returns bounding box expanded in all directions from the bounding box of the input geometry. Uses double-precision",
                            "properties": {
                                "dx": {"format": "double precision", "type": "number"},
                                "dy": {"format": "double precision", "type": "number"},
                                "geom": {"format": "geometry", "type": "string"},
                                "dz": {"format": "double precision", "type": "number"},
                                "dm": {"format": "double precision", "type": "number"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_combinebbox": {
            "post": {
                "tags": ["(rpc) st_combinebbox"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linemerge": {
            "post": {
                "tags": ["(rpc) st_linemerge"],
                "summary": "args: amultilinestring - Return a (set of) LineString(s) formed by sewing together a MULTILINESTRING.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: amultilinestring - Return a (set of) LineString(s) formed by sewing together a MULTILINESTRING.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_decompress": {
            "post": {
                "tags": ["(rpc) geography_gist_decompress"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_typmod_in": {
            "post": {
                "tags": ["(rpc) geometry_typmod_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linefromwkb": {
            "post": {
                "tags": ["(rpc) st_linefromwkb"],
                "summary": "args: WKB, srid - Makes a LINESTRING from WKB with the given SRID",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKB, srid - Makes a LINESTRING from WKB with the given SRID",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multipolygonfromtext": {
            "post": {
                "tags": ["(rpc) st_multipolygonfromtext"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_minconvexhull": {
            "post": {
                "tags": ["(rpc) st_minconvexhull"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_consistent_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_consistent_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_pointoutside": {
            "post": {
                "tags": ["(rpc) _st_pointoutside"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_extent": {
            "post": {
                "tags": ["(rpc) st_extent"],
                "summary": "args: geomfield - an aggregate function that returns the bounding box that bounds rows of geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomfield - an aggregate function that returns the bounding box that bounds rows of geometries.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_polygonize_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_polygonize_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_colormap": {
            "post": {
                "tags": ["(rpc) _st_colormap"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "colormap"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "colormap": {"format": "text", "type": "string"},
                                "method": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linefromencodedpolyline": {
            "post": {
                "tags": ["(rpc) st_linefromencodedpolyline"],
                "summary": "args: polyline, precision=5 - Creates a LineString from an Encoded Polyline.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: polyline, precision=5 - Creates a LineString from an Encoded Polyline.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_numpatches": {
            "post": {
                "tags": ["(rpc) st_numpatches"],
                "summary": "args: g1 - Return the number of faces on a Polyhedral Surface. Will return null for non-polyhedral geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the number of faces on a Polyhedral Surface. Will return null for non-polyhedral geometries.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3ddwithin": {
            "post": {
                "tags": ["(rpc) st_3ddwithin"],
                "summary": "args: g1, g2, distance_of_srid - For 3d (z) geometry type Returns true if two geometries 3d distance is within number of units.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2", "double"],
                            "type": "object",
                            "description": "args: g1, g2, distance_of_srid - For 3d (z) geometry type Returns true if two geometries 3d distance is within number of units.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"},
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gt": {
            "post": {
                "tags": ["(rpc) geometry_gt"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setsrid": {
            "post": {
                "tags": ["(rpc) st_setsrid"],
                "summary": "args: rast, srid - Sets the SRID of a raster to a particular integer srid defined in the spatial_ref_sys table.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "srid"],
                            "type": "object",
                            "description": "args: rast, srid - Sets the SRID of a raster to a particular integer srid defined in the spatial_ref_sys table.",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "rast": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makepoint": {
            "post": {
                "tags": ["(rpc) st_makepoint"],
                "summary": "args: x, y, z, m - Creates a 2D,3DZ or 4D point geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double", "double"],
                            "type": "object",
                            "description": "args: x, y, z, m - Creates a 2D,3DZ or 4D point geometry.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setrotation": {
            "post": {
                "tags": ["(rpc) st_setrotation"],
                "summary": "args: rast, rotation - Set the rotation of the raster in radian.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "rotation"],
                            "type": "object",
                            "description": "args: rast, rotation - Set the rotation of the raster in radian.",
                            "properties": {
                                "rotation": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rast": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setpoint": {
            "post": {
                "tags": ["(rpc) st_setpoint"],
                "summary": "args: linestring, zerobasedposition, point - Replace point of a linestring with a given point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: linestring, zerobasedposition, point - Replace point of a linestring with a given point.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multipointfromtext": {
            "post": {
                "tags": ["(rpc) st_multipointfromtext"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makepolygon": {
            "post": {
                "tags": ["(rpc) st_makepolygon"],
                "summary": "args: outerlinestring, interiorlinestrings - Creates a Polygon formed by the given shell. Input geometries must be closed LINESTRINGS.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: outerlinestring, interiorlinestrings - Creates a Polygon formed by the given shell. Input geometries must be closed LINESTRINGS.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_translate": {
            "post": {
                "tags": ["(rpc) st_translate"],
                "summary": "args: g1, deltax, deltay, deltaz - Translate a geometry by given offsets.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double"],
                            "type": "object",
                            "description": "args: g1, deltax, deltay, deltaz - Translate a geometry by given offsets.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_dwithin": {
            "post": {
                "tags": ["(rpc) _st_dwithin"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "nband1",
                                "rast2",
                                "nband2",
                                "distance",
                            ],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "distance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_out_db": {
            "post": {
                "tags": ["(rpc) _raster_constraint_out_db"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_left": {
            "post": {
                "tags": ["(rpc) geometry_left"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geom4d_brin_inclusion_add_value": {
            "post": {
                "tags": ["(rpc) geom4d_brin_inclusion_add_value"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_3ddfullywithin": {
            "post": {
                "tags": ["(rpc) _st_3ddfullywithin"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2", "double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"},
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_union": {
            "post": {
                "tags": ["(rpc) st_union"],
                "summary": "args: g1, g2 - Returns a geometry that represents the point set union of the Geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns a geometry that represents the point set union of the Geometries.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_touches": {
            "post": {
                "tags": ["(rpc) st_touches"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA and rastB have at least one point in common but their interiors do not intersect.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA and rastB have at least one point in common but their interiors do not intersect.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_transform_geometry": {
            "post": {
                "tags": ["(rpc) postgis_transform_geometry"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_shiftlongitude": {
            "post": {
                "tags": ["(rpc) st_shiftlongitude"],
                "summary": "args: geomA - Toggle geometry coordinates between -180..180 and 0..360 ranges.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Toggle geometry coordinates between -180..180 and 0..360 ranges.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_clusterwithin_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_clusterwithin_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_overright": {
            "post": {
                "tags": ["(rpc) geometry_overright"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rotatez": {
            "post": {
                "tags": ["(rpc) st_rotatez"],
                "summary": "args: geomA, rotRadians - Rotate a geometry rotRadians about the Z axis.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: geomA, rotRadians - Rotate a geometry rotRadians about the Z axis.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_pixel_types": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_pixel_types"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_retile": {
            "post": {
                "tags": ["(rpc) st_retile"],
                "summary": "args: tab, col, ext, sfx, sfy, tw, th, algo='NearestNeighbor' - Return a set of configured tiles from an arbitrarily tiled raster coverage.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["tab", "col", "ext", "sfx", "sfy", "tw", "th"],
                            "type": "object",
                            "description": "args: tab, col, ext, sfx, sfy, tw, th, algo='NearestNeighbor' - Return a set of configured tiles from an arbitrarily tiled raster coverage.",
                            "properties": {
                                "sfy": {"format": "double precision", "type": "number"},
                                "th": {"format": "integer", "type": "integer"},
                                "sfx": {"format": "double precision", "type": "number"},
                                "tab": {"format": "regclass", "type": "string"},
                                "algo": {"format": "text", "type": "string"},
                                "col": {"format": "name", "type": "string"},
                                "tw": {"format": "integer", "type": "integer"},
                                "ext": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_fromgdalraster": {
            "post": {
                "tags": ["(rpc) st_fromgdalraster"],
                "summary": "args: gdaldata, srid=NULL - Returns a raster from a supported GDAL raster file.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["gdaldata"],
                            "type": "object",
                            "description": "args: gdaldata, srid=NULL - Returns a raster from a supported GDAL raster file.",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "gdaldata": {"format": "bytea", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mlinefromwkb": {
            "post": {
                "tags": ["(rpc) st_mlinefromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_constraint_dims": {
            "post": {
                "tags": ["(rpc) postgis_constraint_dims"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geomschema", "geomtable", "geomcolumn"],
                            "type": "object",
                            "properties": {
                                "geomschema": {"format": "text", "type": "string"},
                                "geomcolumn": {"format": "text", "type": "string"},
                                "geomtable": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mapalgebrafct": {
            "post": {
                "tags": ["(rpc) st_mapalgebrafct"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "band1",
                                "rast2",
                                "band2",
                                "tworastuserfunc",
                            ],
                            "type": "object",
                            "properties": {
                                "tworastuserfunc": {
                                    "format": "regprocedure",
                                    "type": "string",
                                },
                                "rast1": {"format": "raster", "type": "string"},
                                "band1": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "rast2": {"format": "raster", "type": "string"},
                                "band2": {"format": "integer", "type": "integer"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                                "extenttype": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_in": {
            "post": {
                "tags": ["(rpc) raster_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_ymin": {
            "post": {
                "tags": ["(rpc) st_ymin"],
                "summary": "args: aGeomorBox2DorBox3D - Returns Y minima of a bounding box 2d or 3d or a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aGeomorBox2DorBox3D - Returns Y minima of a bounding box 2d or 3d or a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_count": {
            "post": {
                "tags": ["(rpc) st_count"],
                "summary": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true - Returns the number of pixels in a given band of a raster or raster coverage. If no band is specified defaults to band 1. If exclude_nodata_value is set to true, will only count pixels that are not equal to the nodata value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "description": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true - Returns the number of pixels in a given band of a raster or raster coverage. If no band is specified defaults to band 1. If exclude_nodata_value is set to true, will only count pixels that are not equal to the nodata value.",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_contains": {
            "post": {
                "tags": ["(rpc) st_contains"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastB lie in the exterior of raster rastA and at least one point of the interior of rastB lies in the interior of rastA.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastB lie in the exterior of raster rastA and at least one point of the interior of rastB lies in the interior of rastA.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geomfromewkt": {
            "post": {
                "tags": ["(rpc) geomfromewkt"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_wkbtosql": {
            "post": {
                "tags": ["(rpc) st_wkbtosql"],
                "summary": "args: WKB - Return a specified ST_Geometry value from Well-Known Binary representation (WKB). This is an alias name for ST_GeomFromWKB that takes no srid",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["wkb"],
                            "type": "object",
                            "description": "args: WKB - Return a specified ST_Geometry value from Well-Known Binary representation (WKB). This is an alias name for ST_GeomFromWKB that takes no srid",
                            "properties": {
                                "wkb": {"format": "bytea", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_regular_blocking": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_regular_blocking"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dumppoints": {
            "post": {
                "tags": ["(rpc) st_dumppoints"],
                "summary": "args: geom - Returns a set of geometry_dump (geom,path) rows of all points that make up a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom - Returns a set of geometry_dump (geom,path) rows of all points that make up a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gserialized_gist_sel_nd": {
            "post": {
                "tags": ["(rpc) gserialized_gist_sel_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_abs_out": {
            "post": {
                "tags": ["(rpc) pgis_abs_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromtext": {
            "post": {
                "tags": ["(rpc) st_geomfromtext"],
                "summary": "args: WKT, srid - Return a specified ST_Geometry value from Well-Known Text representation (WKT).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Return a specified ST_Geometry value from Well-Known Text representation (WKT).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setgeotransform": {
            "post": {
                "tags": ["(rpc) st_setgeotransform"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast",
                                "imag",
                                "jmag",
                                "theta_i",
                                "theta_ij",
                                "xoffset",
                                "yoffset",
                            ],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "yoffset": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "imag": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "theta_i": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "xoffset": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "theta_ij": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "jmag": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_cmp": {
            "post": {
                "tags": ["(rpc) geometry_cmp"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_zmflag": {
            "post": {
                "tags": ["(rpc) st_zmflag"],
                "summary": "args: geomA - Returns ZM (dimension semantic) flag of the geometries as a small int. Values are: 0=2d, 1=3dm, 2=3dz, 3=4d.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns ZM (dimension semantic) flag of the geometries as a small int. Values are: 0=2d, 1=3dm, 2=3dz, 3=4d.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_containsproperly": {
            "post": {
                "tags": ["(rpc) _st_containsproperly"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_accum_transfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_accum_transfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_clusterintersecting_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_clusterintersecting_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_interpolatepoint": {
            "post": {
                "tags": ["(rpc) st_interpolatepoint"],
                "summary": "args: line, point - Return the value of the measure dimension of a geometry at the point closed to the provided point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["line", "point"],
                            "type": "object",
                            "description": "args: line, point - Return the value of the measure dimension of a geometry at the point closed to the provided point.",
                            "properties": {
                                "line": {"format": "geometry", "type": "string"},
                                "point": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/bytea": {
            "post": {
                "tags": ["(rpc) bytea"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromgeojson": {
            "post": {
                "tags": ["(rpc) st_geomfromgeojson"],
                "summary": "args: geomjson - Takes as input a geojson representation of a geometry and outputs a PostGIS geometry object",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomjson - Takes as input a geojson representation of a geometry and outputs a PostGIS geometry object",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromewkt": {
            "post": {
                "tags": ["(rpc) st_geomfromewkt"],
                "summary": "args: EWKT - Return a specified ST_Geometry value from Extended Well-Known Text representation (EWKT).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: EWKT - Return a specified ST_Geometry value from Extended Well-Known Text representation (EWKT).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dlength": {
            "post": {
                "tags": ["(rpc) st_3dlength"],
                "summary": "args: a_3dlinestring - Returns the 3-dimensional or 2-dimensional length of the geometry if it is a linestring or multi-linestring.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_3dlinestring - Returns the 3-dimensional or 2-dimensional length of the geometry if it is a linestring or multi-linestring.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_raster_lib_build_date": {
            "post": {
                "tags": ["(rpc) postgis_raster_lib_build_date"],
                "summary": "Reports full raster library build date.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Reports full raster library build date.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_eq": {
            "post": {
                "tags": ["(rpc) geography_eq"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dfullywithin": {
            "post": {
                "tags": ["(rpc) st_dfullywithin"],
                "summary": "args: rastA, nbandA, rastB, nbandB, distance_of_srid - Return true if rasters rastA and rastB are fully within the specified distance of each other.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "nband1",
                                "rast2",
                                "nband2",
                                "distance",
                            ],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB, distance_of_srid - Return true if rasters rastA and rastB are fully within the specified distance of each other.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "distance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_value": {
            "post": {
                "tags": ["(rpc) st_value"],
                "summary": "args: rast, band, x, y, exclude_nodata_value=true - Returns the value of a given band in a given columnx, rowy pixel or at a particular geometric point. Band numbers start at 1 and assumed to be 1 if not specified. If exclude_nodata_value is set to false, then all pixels include nodata pixels are considered to intersect and return value. If exclude_nodata_value is not passed in then reads it from metadata of raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "band", "x", "y"],
                            "type": "object",
                            "description": "args: rast, band, x, y, exclude_nodata_value=true - Returns the value of a given band in a given columnx, rowy pixel or at a particular geometric point. Band numbers start at 1 and assumed to be 1 if not specified. If exclude_nodata_value is set to false, then all pixels include nodata pixels are considered to intersect and return value. If exclude_nodata_value is not passed in then reads it from metadata of raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "x": {"format": "integer", "type": "integer"},
                                "band": {"format": "integer", "type": "integer"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box2d": {
            "post": {
                "tags": ["(rpc) box2d"],
                "summary": "args: geomA - Returns a BOX2D representing the maximum extents of the geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns a BOX2D representing the maximum extents of the geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_forcesfs": {
            "post": {
                "tags": ["(rpc) st_forcesfs"],
                "summary": "args: geomA, version - Force the geometries to use SFS 1.1 geometry types only.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["version"],
                            "type": "object",
                            "description": "args: geomA, version - Force the geometries to use SFS 1.1 geometry types only.",
                            "properties": {
                                "version": {"format": "text", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_length2d_spheroid": {
            "post": {
                "tags": ["(rpc) st_length2d_spheroid"],
                "summary": "args: a_geometry, a_spheroid - Calculates the 2D length/perimeter of a geometry on an ellipsoid. This is useful if the coordinates of the geometry are in longitude/latitude and a length is desired without reprojection.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_geometry, a_spheroid - Calculates the 2D length/perimeter of a geometry on an ellipsoid. This is useful if the coordinates of the geometry are in longitude/latitude and a length is desired without reprojection.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force2d": {
            "post": {
                "tags": ["(rpc) st_force2d"],
                "summary": 'args: geomA - Force the geometries into a "2-dimensional mode".',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": 'args: geomA - Force the geometries into a "2-dimensional mode".',
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box2d_in": {
            "post": {
                "tags": ["(rpc) box2d_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_pixel_types": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_pixel_types"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_collectionextract": {
            "post": {
                "tags": ["(rpc) st_collectionextract"],
                "summary": "args: collection, type - Given a (multi)geometry, return a (multi)geometry consisting only of elements of the specified type.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: collection, type - Given a (multi)geometry, return a (multi)geometry consisting only of elements of the specified type.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_out": {
            "post": {
                "tags": ["(rpc) geometry_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_estimated_extent": {
            "post": {
                "tags": ["(rpc) st_estimated_extent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_endpoint": {
            "post": {
                "tags": ["(rpc) st_endpoint"],
                "summary": "args: g - Returns the last point of a LINESTRING or CIRCULARLINESTRING geometry as a POINT.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Returns the last point of a LINESTRING or CIRCULARLINESTRING geometry as a POINT.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geometricmedian": {
            "post": {
                "tags": ["(rpc) st_geometricmedian"],
                "summary": "args: ",
                "description": "\t\t\t\t\tg\n\t\t\t\t, \n\t\t\t\t\ttolerance\n\t\t\t\t, \n\t\t\t\t\tmax_iter\n\t\t\t\t, \n\t\t\t\t\tfail_if_not_converged\n\t\t\t\t - Returns the geometric median of a MultiPoint.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["g"],
                            "type": "object",
                            "description": "args: \n\t\t\t\t\tg\n\t\t\t\t, \n\t\t\t\t\ttolerance\n\t\t\t\t, \n\t\t\t\t\tmax_iter\n\t\t\t\t, \n\t\t\t\t\tfail_if_not_converged\n\t\t\t\t - Returns the geometric median of a MultiPoint.",
                            "properties": {
                                "g": {"format": "geometry", "type": "string"},
                                "fail_if_not_converged": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "max_iter": {"format": "integer", "type": "integer"},
                                "tolerance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setgeoreference": {
            "post": {
                "tags": ["(rpc) st_setgeoreference"],
                "summary": "args: rast, upperleftx, upperlefty, scalex, scaley, skewx, skewy - Set Georeference 6 georeference parameters in a single call. Numbers should be separated by white space. Accepts inputs in GDAL or ESRI format. Default is GDAL.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast",
                                "upperleftx",
                                "upperlefty",
                                "scalex",
                                "scaley",
                                "skewx",
                                "skewy",
                            ],
                            "type": "object",
                            "description": "args: rast, upperleftx, upperlefty, scalex, scaley, skewx, skewy - Set Georeference 6 georeference parameters in a single call. Numbers should be separated by white space. Accepts inputs in GDAL or ESRI format. Default is GDAL.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "upperlefty": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "upperleftx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3ddistance": {
            "post": {
                "tags": ["(rpc) st_3ddistance"],
                "summary": "args: g1, g2 - For geometry type Returns the 3-dimensional cartesian minimum distance (based on spatial ref) between two geometries in projected units.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - For geometry type Returns the 3-dimensional cartesian minimum distance (based on spatial ref) between two geometries in projected units.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_same_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_same_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/droprasterconstraints": {
            "post": {
                "tags": ["(rpc) droprasterconstraints"],
                "summary": "args: rastschema, rasttable, rastcolumn, srid=true, scale_x=true, scale_y=true, blocksize_x=true, blocksize_y=true, same_alignment=true, regular_blocking=false, num_bands=true, pixel_types=true, nodata_values=true, out_db=true, extent=true - Drops PostGIS raster constraints that refer to a raster table column. Useful if you need to reload data or update your raster column data.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "description": "args: rastschema, rasttable, rastcolumn, srid=true, scale_x=true, scale_y=true, blocksize_x=true, blocksize_y=true, same_alignment=true, regular_blocking=false, num_bands=true, pixel_types=true, nodata_values=true, out_db=true, extent=true - Drops PostGIS raster constraints that refer to a raster table column. Useful if you need to reload data or update your raster column data.",
                            "properties": {
                                "srid": {"format": "boolean", "type": "boolean"},
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "num_bands": {"format": "boolean", "type": "boolean"},
                                "extent": {"format": "boolean", "type": "boolean"},
                                "scale_y": {"format": "boolean", "type": "boolean"},
                                "pixel_types": {"format": "boolean", "type": "boolean"},
                                "regular_blocking": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "out_db": {"format": "boolean", "type": "boolean"},
                                "scale_x": {"format": "boolean", "type": "boolean"},
                                "same_alignment": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "blocksize_y": {"format": "boolean", "type": "boolean"},
                                "blocksize_x": {"format": "boolean", "type": "boolean"},
                                "nodata_values": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_numinteriorring": {
            "post": {
                "tags": ["(rpc) st_numinteriorring"],
                "summary": "args: a_polygon - Return the number of interior rings of a polygon in the geometry. Synonym for ST_NumInteriorRings.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_polygon - Return the number of interior rings of a polygon in the geometry. Synonym for ST_NumInteriorRings.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_summarystatsagg": {
            "post": {
                "tags": ["(rpc) st_summarystatsagg"],
                "summary": "args: rast, nband, exclude_nodata_value, sample_percent - Aggregate. Returns summarystats consisting of count, sum, mean, stddev, min, max for a given raster band of a set of raster. Band 1 is assumed is no band is specified.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: rast, nband, exclude_nodata_value, sample_percent - Aggregate. Returns summarystats consisting of count, sum, mean, stddev, min, max for a given raster band of a set of raster. Band 1 is assumed is no band is specified.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromkml": {
            "post": {
                "tags": ["(rpc) st_geomfromkml"],
                "summary": "args: geomkml - Takes as input KML representation of geometry and outputs a PostGIS geometry object",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomkml - Takes as input KML representation of geometry and outputs a PostGIS geometry object",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/addoverviewconstraints": {
            "post": {
                "tags": ["(rpc) addoverviewconstraints"],
                "summary": "args: ovschema, ovtable, ovcolumn, refschema, reftable, refcolumn, ovfactor - Tag a raster column as being an overview of another.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "ovschema",
                                "ovtable",
                                "ovcolumn",
                                "refschema",
                                "reftable",
                                "refcolumn",
                                "ovfactor",
                            ],
                            "type": "object",
                            "description": "args: ovschema, ovtable, ovcolumn, refschema, reftable, refcolumn, ovfactor - Tag a raster column as being an overview of another.",
                            "properties": {
                                "ovfactor": {"format": "integer", "type": "integer"},
                                "ovcolumn": {"format": "name", "type": "string"},
                                "reftable": {"format": "name", "type": "string"},
                                "ovschema": {"format": "name", "type": "string"},
                                "ovtable": {"format": "name", "type": "string"},
                                "refcolumn": {"format": "name", "type": "string"},
                                "refschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_distance_box": {
            "post": {
                "tags": ["(rpc) geometry_distance_box"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_spatially_unique": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_spatially_unique"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_pixel_types": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_pixel_types"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_constraint_srid": {
            "post": {
                "tags": ["(rpc) postgis_constraint_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geomschema", "geomtable", "geomcolumn"],
                            "type": "object",
                            "properties": {
                                "geomschema": {"format": "text", "type": "string"},
                                "geomcolumn": {"format": "text", "type": "string"},
                                "geomtable": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_summary": {
            "post": {
                "tags": ["(rpc) st_summary"],
                "summary": "args: rast - Returns a text summary of the contents of the raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast - Returns a text summary of the contents of the raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_ashexewkb": {
            "post": {
                "tags": ["(rpc) st_ashexewkb"],
                "summary": "args: g1, NDRorXDR - Returns a Geometry in HEXEWKB format (as text) using either little-endian (NDR) or big-endian (XDR) encoding.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1, NDRorXDR - Returns a Geometry in HEXEWKB format (as text) using either little-endian (NDR) or big-endian (XDR) encoding.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_approxhistogram": {
            "post": {
                "tags": ["(rpc) st_approxhistogram"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "width": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                                "right": {"format": "boolean", "type": "boolean"},
                                "bins": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_full_version": {
            "post": {
                "tags": ["(rpc) postgis_full_version"],
                "summary": "Reports full postgis version and build configuration infos.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Reports full postgis version and build configuration infos.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_contained_by_geometry": {
            "post": {
                "tags": ["(rpc) raster_contained_by_geometry"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_convexhull": {
            "post": {
                "tags": ["(rpc) st_convexhull"],
                "summary": "args: geomA - The convex hull of a geometry represents the minimum convex geometry that encloses all geometries within the set.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - The convex hull of a geometry represents the minimum convex geometry that encloses all geometries within the set.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_generatepoints": {
            "post": {
                "tags": ["(rpc) st_generatepoints"],
                "summary": "args: g, npoints - Converts a polygon or multi-polygon into a multi-point composed of randomly location points within the original areas.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["area", "npoints"],
                            "type": "object",
                            "description": "args: g, npoints - Converts a polygon or multi-polygon into a multi-point composed of randomly location points within the original areas.",
                            "properties": {
                                "area": {"format": "geometry", "type": "string"},
                                "npoints": {"format": "numeric", "type": "number"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gt": {
            "post": {
                "tags": ["(rpc) geography_gt"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_transform": {
            "post": {
                "tags": ["(rpc) st_transform"],
                "summary": "args: rast, srid, scalex, scaley, algorithm=NearestNeighbor, maxerr=0.125 - Reprojects a raster in a known spatial reference system to another known spatial reference system using specified resampling algorithm. Options are NearestNeighbor, Bilinear, Cubic, CubicSpline, Lanczos defaulting to NearestNeighbor.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "srid", "scalex", "scaley"],
                            "type": "object",
                            "description": "args: rast, srid, scalex, scaley, algorithm=NearestNeighbor, maxerr=0.125 - Reprojects a raster in a known spatial reference system to another known spatial reference system using specified resampling algorithm. Options are NearestNeighbor, Bilinear, Cubic, CubicSpline, Lanczos defaulting to NearestNeighbor.",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "rast": {"format": "raster", "type": "string"},
                                "algorithm": {"format": "text", "type": "string"},
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_svn_version": {
            "post": {
                "tags": ["(rpc) postgis_svn_version"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_distance": {
            "post": {
                "tags": ["(rpc) _st_distance"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_addbbox": {
            "post": {
                "tags": ["(rpc) postgis_addbbox"],
                "summary": "args: geomA - Add bounding box to the geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Add bounding box to the geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makeemptyraster": {
            "post": {
                "tags": ["(rpc) st_makeemptyraster"],
                "summary": "args: width, height, upperleftx, upperlefty, scalex, scaley, skewx, skewy, srid=unknown - Returns an empty raster (having no bands) of given dimensions (width & height), upperleft X and Y, pixel size and rotation (scalex, scaley, skewx & skewy) and reference system (srid). If a raster is passed in, returns a new raster with the same size, alignment and SRID. If srid is left out, the spatial ref is set to unknown (0).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "width",
                                "height",
                                "upperleftx",
                                "upperlefty",
                                "scalex",
                                "scaley",
                                "skewx",
                                "skewy",
                            ],
                            "type": "object",
                            "description": "args: width, height, upperleftx, upperlefty, scalex, scaley, skewx, skewy, srid=unknown - Returns an empty raster (having no bands) of given dimensions (width & height), upperleft X and Y, pixel size and rotation (scalex, scaley, skewx & skewy) and reference system (srid). If a raster is passed in, returns a new raster with the same size, alignment and SRID. If srid is left out, the spatial ref is set to unknown (0).",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "height": {"format": "integer", "type": "integer"},
                                "upperlefty": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "upperleftx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_startpoint": {
            "post": {
                "tags": ["(rpc) st_startpoint"],
                "summary": "args: geomA - Returns the first point of a LINESTRING geometry as a POINT.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns the first point of a LINESTRING geometry as a POINT.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_contained_by_raster": {
            "post": {
                "tags": ["(rpc) geometry_contained_by_raster"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geometryn": {
            "post": {
                "tags": ["(rpc) st_geometryn"],
                "summary": "args: geomA, n - Return the 1-based Nth geometry if the geometry is a GEOMETRYCOLLECTION, (MULTI)POINT, (MULTI)LINESTRING, MULTICURVE or (MULTI)POLYGON, POLYHEDRALSURFACE Otherwise, return NULL.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA, n - Return the 1-based Nth geometry if the geometry is a GEOMETRYCOLLECTION, (MULTI)POINT, (MULTI)LINESTRING, MULTICURVE or (MULTI)POLYGON, POLYHEDRALSURFACE Otherwise, return NULL.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_typmod_in": {
            "post": {
                "tags": ["(rpc) geography_typmod_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makeenvelope": {
            "post": {
                "tags": ["(rpc) st_makeenvelope"],
                "summary": "args: xmin, ymin, xmax, ymax, srid=unknown - Creates a rectangular Polygon formed from the given minimums and maximums. Input values must be in SRS specified by the SRID.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double", "double"],
                            "type": "object",
                            "description": "args: xmin, ymin, xmax, ymax, srid=unknown - Creates a rectangular Polygon formed from the given minimums and maximums. Input values must be in SRS specified by the SRID.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_count": {
            "post": {
                "tags": ["(rpc) _st_count"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_srid": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_touches": {
            "post": {
                "tags": ["(rpc) _st_touches"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_interiorringn": {
            "post": {
                "tags": ["(rpc) st_interiorringn"],
                "summary": "args: a_polygon, n - Return the Nth interior linestring ring of the polygon geometry. Return NULL if the geometry is not a polygon or the given N is out of range.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_polygon, n - Return the Nth interior linestring ring of the polygon geometry. Return NULL if the geometry is not a polygon or the given N is out of range.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_length2dspheroid": {
            "post": {
                "tags": ["(rpc) st_length2dspheroid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_scripts_build_date": {
            "post": {
                "tags": ["(rpc) postgis_scripts_build_date"],
                "summary": "Returns build date of the PostGIS scripts.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns build date of the PostGIS scripts.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_spatially_unique": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_spatially_unique"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_contain": {
            "post": {
                "tags": ["(rpc) raster_contain"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geom3d_brin_inclusion_add_value": {
            "post": {
                "tags": ["(rpc) geom3d_brin_inclusion_add_value"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_noop": {
            "post": {
                "tags": ["(rpc) postgis_noop"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box2df_out": {
            "post": {
                "tags": ["(rpc) box2df_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_estimatedextent": {
            "post": {
                "tags": ["(rpc) st_estimatedextent"],
                "summary": "args: table_name, geocolumn_name - Return the estimated extent of the given spatial table. The estimated is taken from the geometry columns statistics. The current schema will be used if not specified.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: table_name, geocolumn_name - Return the estimated extent of the given spatial table. The estimated is taken from the geometry columns statistics. The current schema will be used if not specified.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_notsamealignmentreason": {
            "post": {
                "tags": ["(rpc) st_notsamealignmentreason"],
                "summary": "args: rastA, rastB - Returns text stating if rasters are aligned and if not aligned, a reason why.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "rast2"],
                            "type": "object",
                            "description": "args: rastA, rastB - Returns text stating if rasters are aligned and if not aligned, a reason why.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_postgis_stats": {
            "post": {
                "tags": ["(rpc) _postgis_stats"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["tbl", "att_name"],
                            "type": "object",
                            "properties": {
                                "tbl": {"format": "regclass", "type": "string"},
                                "att_name": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force_collection": {
            "post": {
                "tags": ["(rpc) st_force_collection"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bandpath": {
            "post": {
                "tags": ["(rpc) st_bandpath"],
                "summary": "args: rast, bandnum=1 - Returns system file path to a band stored in file system. If no bandnum specified, 1 is assumed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, bandnum=1 - Returns system file path to a band stored in file system. If no bandnum specified, 1 is assumed.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dump": {
            "post": {
                "tags": ["(rpc) st_dump"],
                "summary": "args: g1 - Returns a set of geometry_dump (geom,path) rows, that make up a geometry g1.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Returns a set of geometry_dump (geom,path) rows, that make up a geometry g1.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_xmax": {
            "post": {
                "tags": ["(rpc) st_xmax"],
                "summary": "args: aGeomorBox2DorBox3D - Returns X maxima of a bounding box 2d or 3d or a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aGeomorBox2DorBox3D - Returns X maxima of a bounding box 2d or 3d or a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_tile": {
            "post": {
                "tags": ["(rpc) st_tile"],
                "summary": "args: rast, nband, width, height, padwithnodata=FALSE, nodataval=NULL - Returns a set of rasters resulting from the split of the input raster based upon the desired dimensions of the output rasters.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "width", "height"],
                            "type": "object",
                            "description": "args: rast, nband, width, height, padwithnodata=FALSE, nodataval=NULL - Returns a set of rasters resulting from the split of the input raster based upon the desired dimensions of the output rasters.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "height": {"format": "integer", "type": "integer"},
                                "nband": {"format": "integer[]", "type": "string"},
                                "nodataval": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "padwithnodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomcollfromwkb": {
            "post": {
                "tags": ["(rpc) st_geomcollfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asencodedpolyline": {
            "post": {
                "tags": ["(rpc) st_asencodedpolyline"],
                "summary": "args: geom, precision=5 - Returns an Encoded Polyline from a LineString geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom, precision=5 - Returns an Encoded Polyline from a LineString geometry.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_overabove": {
            "post": {
                "tags": ["(rpc) geometry_overabove"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_wrapx": {
            "post": {
                "tags": ["(rpc) st_wrapx"],
                "summary": "args: geom, wrap, move - Wrap a geometry around an X value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "wrap", "move"],
                            "type": "object",
                            "description": "args: geom, wrap, move - Wrap a geometry around an X value.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "wrap": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "move": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dumpvalues": {
            "post": {
                "tags": ["(rpc) st_dumpvalues"],
                "summary": "args: rast, nband=NULL, exclude_nodata_value=true - Get the values of the specified band as a 2-dimension array.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, nband=NULL, exclude_nodata_value=true - Get the values of the specified band as a 2-dimension array.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer[]", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_find_extent": {
            "post": {
                "tags": ["(rpc) st_find_extent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multi": {
            "post": {
                "tags": ["(rpc) st_multi"],
                "summary": "args: g1 - Return the geometry as a MULTI* geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the geometry as a MULTI* geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bandpixeltype": {
            "post": {
                "tags": ["(rpc) st_bandpixeltype"],
                "summary": "args: rast, bandnum=1 - Returns the type of pixel for given band. If no bandnum specified, 1 is assumed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, bandnum=1 - Returns the type of pixel for given band. If no bandnum specified, 1 is assumed.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dwithin": {
            "post": {
                "tags": ["(rpc) st_dwithin"],
                "summary": "args: rastA, nbandA, rastB, nbandB, distance_of_srid - Return true if rasters rastA and rastB are within the specified distance of each other.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "nband1",
                                "rast2",
                                "nband2",
                                "distance",
                            ],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB, distance_of_srid - Return true if rasters rastA and rastB are within the specified distance of each other.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "distance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_cmp": {
            "post": {
                "tags": ["(rpc) geography_cmp"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gserialized_gist_joinsel_nd": {
            "post": {
                "tags": ["(rpc) gserialized_gist_joinsel_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geog_brin_inclusion_add_value": {
            "post": {
                "tags": ["(rpc) geog_brin_inclusion_add_value"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dumpaspolygons": {
            "post": {
                "tags": ["(rpc) st_dumpaspolygons"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_band": {
            "post": {
                "tags": ["(rpc) st_band"],
                "summary": "args: rast, nbands, delimiter=, - Returns one or more bands of an existing raster as a new raster. Useful for building new rasters from existing rasters.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nbands"],
                            "type": "object",
                            "description": "args: rast, nbands, delimiter=, - Returns one or more bands of an existing raster as a new raster. Useful for building new rasters from existing rasters.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nbands": {"format": "text", "type": "string"},
                                "delimiter": {"format": "character", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mpointfromwkb": {
            "post": {
                "tags": ["(rpc) st_mpointfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_overbelow": {
            "post": {
                "tags": ["(rpc) raster_overbelow"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_decompress_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_decompress_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rotate": {
            "post": {
                "tags": ["(rpc) st_rotate"],
                "summary": "args: geomA, rotRadians, x0, y0 - Rotate a geometry rotRadians counter-clockwise about an origin.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double"],
                            "type": "object",
                            "description": "args: geomA, rotRadians, x0, y0 - Rotate a geometry rotRadians counter-clockwise about an origin.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dshortestline": {
            "post": {
                "tags": ["(rpc) st_3dshortestline"],
                "summary": "args: g1, g2 - Returns the 3-dimensional shortest line between two geometries",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 3-dimensional shortest line between two geometries",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_locate_between_measures": {
            "post": {
                "tags": ["(rpc) st_locate_between_measures"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_neighborhood": {
            "post": {
                "tags": ["(rpc) _st_neighborhood"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast",
                                "band",
                                "columnx",
                                "rowy",
                                "distancex",
                                "distancey",
                            ],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "distancey": {"format": "integer", "type": "integer"},
                                "rowy": {"format": "integer", "type": "integer"},
                                "distancex": {"format": "integer", "type": "integer"},
                                "columnx": {"format": "integer", "type": "integer"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_voronoilines": {
            "post": {
                "tags": ["(rpc) st_voronoilines"],
                "summary": "args: g1, tolerance, extend_to - Returns the boundaries between the cells of the Voronoi diagram constructed from the vertices of a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["g1"],
                            "type": "object",
                            "description": "args: g1, tolerance, extend_to - Returns the boundaries between the cells of the Voronoi diagram constructed from the vertices of a geometry.",
                            "properties": {
                                "extend_to": {"format": "geometry", "type": "string"},
                                "g1": {"format": "geometry", "type": "string"},
                                "tolerance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_samealignment_finalfn": {
            "post": {
                "tags": ["(rpc) _st_samealignment_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["agg"],
                            "type": "object",
                            "properties": {
                                "agg": {"format": "agg_samealignment", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/addauth": {
            "post": {
                "tags": ["(rpc) addauth"],
                "summary": "args: auth_token - Add an authorization token to be used in current transaction.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: auth_token - Add an authorization token to be used in current transaction.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/create_json_where": {
            "post": {
                "tags": ["(rpc) create_json_where"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["_key", "_value"],
                            "type": "object",
                            "properties": {
                                "_value": {"format": "json", "type": "string"},
                                "_key": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_extent": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_extent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geogfromtext": {
            "post": {
                "tags": ["(rpc) st_geogfromtext"],
                "summary": "args: EWKT - Return a specified geography value from Well-Known Text representation or extended (WKT).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: EWKT - Return a specified geography value from Well-Known Text representation or extended (WKT).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_covers": {
            "post": {
                "tags": ["(rpc) _st_covers"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_eq": {
            "post": {
                "tags": ["(rpc) geometry_eq"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_intersects": {
            "post": {
                "tags": ["(rpc) _st_intersects"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_clip": {
            "post": {
                "tags": ["(rpc) _st_clip"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "geom"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer[]", "type": "string"},
                                "nodataval": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "geom": {"format": "geometry", "type": "string"},
                                "crop": {"format": "boolean", "type": "boolean"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_geos_version": {
            "post": {
                "tags": ["(rpc) postgis_geos_version"],
                "summary": "Returns the version number of the GEOS library.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns the version number of the GEOS library.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_overleft": {
            "post": {
                "tags": ["(rpc) raster_overleft"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_orderingequals": {
            "post": {
                "tags": ["(rpc) st_orderingequals"],
                "summary": "args: A, B - Returns true if the given geometries represent the same geometry and points are in the same directional order.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometrya", "geometryb"],
                            "type": "object",
                            "description": "args: A, B - Returns true if the given geometries represent the same geometry and points are in the same directional order.",
                            "properties": {
                                "geometryb": {"format": "geometry", "type": "string"},
                                "geometrya": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_scaley": {
            "post": {
                "tags": ["(rpc) st_scaley"],
                "summary": "args: rast - Returns the Y component of the pixel height in units of coordinate reference system.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the Y component of the pixel height in units of coordinate reference system.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asraster": {
            "post": {
                "tags": ["(rpc) st_asraster"],
                "summary": "args: geom, width, height, pixeltype, value=ARRAY[1], nodataval=ARRAY[0], upperleftx=NULL, upperlefty=NULL, skewx=0, skewy=0, touched=false - Converts a PostGIS geometry to a PostGIS raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "width", "height", "pixeltype"],
                            "type": "object",
                            "description": "args: geom, width, height, pixeltype, value=ARRAY[1], nodataval=ARRAY[0], upperleftx=NULL, upperlefty=NULL, skewx=0, skewy=0, touched=false - Converts a PostGIS geometry to a PostGIS raster.",
                            "properties": {
                                "touched": {"format": "boolean", "type": "boolean"},
                                "height": {"format": "integer", "type": "integer"},
                                "nodataval": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "geom": {"format": "geometry", "type": "string"},
                                "pixeltype": {"format": "text[]", "type": "string"},
                                "upperlefty": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "upperleftx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_geometry_contain": {
            "post": {
                "tags": ["(rpc) raster_geometry_contain"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_out": {
            "post": {
                "tags": ["(rpc) geography_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_scripts_installed": {
            "post": {
                "tags": ["(rpc) postgis_scripts_installed"],
                "summary": "Returns version of the postgis scripts installed in this database.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns version of the postgis scripts installed in this database.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_convertarray4ma": {
            "post": {
                "tags": ["(rpc) _st_convertarray4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                }
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_polyfromtext": {
            "post": {
                "tags": ["(rpc) st_polyfromtext"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_gdal_version": {
            "post": {
                "tags": ["(rpc) postgis_gdal_version"],
                "summary": "Reports the version of the GDAL library in use by PostGIS.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Reports the version of the GDAL library in use by PostGIS.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multilinestringfromtext": {
            "post": {
                "tags": ["(rpc) st_multilinestringfromtext"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_approxsummarystats": {
            "post": {
                "tags": ["(rpc) st_approxsummarystats"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distancecpa": {
            "post": {
                "tags": ["(rpc) st_distancecpa"],
                "summary": "args: track1, track2 - Returns the distance between closest points of approach in two trajectories.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: track1, track2 - Returns the distance between closest points of approach in two trajectories.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_3ddwithin": {
            "post": {
                "tags": ["(rpc) _st_3ddwithin"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2", "double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"},
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setbandnodatavalue": {
            "post": {
                "tags": ["(rpc) st_setbandnodatavalue"],
                "summary": "args: rast, band, nodatavalue, forcechecking=false - Sets the value for the given band that represents no data. Band 1 is assumed if no band is specified. To mark a band as having no nodata value, set the nodata value = NULL.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "band", "nodatavalue"],
                            "type": "object",
                            "description": "args: rast, band, nodatavalue, forcechecking=false - Sets the value for the given band that represents no data. Band 1 is assumed if no band is specified. To mark a band as having no nodata value, set the nodata value = NULL.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nodatavalue": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "forcechecking": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dintersects": {
            "post": {
                "tags": ["(rpc) st_3dintersects"],
                "summary": 'args: geomA, geomB - Returns TRUE if the Geometries "spatially intersect" in 3d - only for points, linestrings, polygons, polyhedral surface (area). With SFCGAL backend enabled also supports TINS',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": 'args: geomA, geomB - Returns TRUE if the Geometries "spatially intersect" in 3d - only for points, linestrings, polygons, polyhedral surface (area). With SFCGAL backend enabled also supports TINS',
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromgeohash": {
            "post": {
                "tags": ["(rpc) st_geomfromgeohash"],
                "summary": "args: geohash, precision=full_precision_of_geohash - Return a geometry from a GeoHash string.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geohash, precision=full_precision_of_geohash - Return a geometry from a GeoHash string.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_extent": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_extent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_point_inside_circle": {
            "post": {
                "tags": ["(rpc) st_point_inside_circle"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_line_locate_point": {
            "post": {
                "tags": ["(rpc) st_line_locate_point"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry": {
            "post": {
                "tags": ["(rpc) geometry"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_curvetoline": {
            "post": {
                "tags": ["(rpc) st_curvetoline"],
                "summary": "args: curveGeom, segments_per_qtr_circle - Converts a CIRCULARSTRING/CURVEPOLYGON to a LINESTRING/POLYGON",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: curveGeom, segments_per_qtr_circle - Converts a CIRCULARSTRING/CURVEPOLYGON to a LINESTRING/POLYGON",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_hasnoband": {
            "post": {
                "tags": ["(rpc) st_hasnoband"],
                "summary": "args: rast, bandnum=1 - Returns true if there is no band with given band number. If no band number is specified, then band number 1 is assumed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, bandnum=1 - Returns true if there is no band with given band number. If no band number is specified, then band number 1 is assumed.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_removepoint": {
            "post": {
                "tags": ["(rpc) st_removepoint"],
                "summary": "args: linestring, offset - Remove point from a linestring.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: linestring, offset - Remove point from a linestring.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_summarystats": {
            "post": {
                "tags": ["(rpc) _st_summarystats"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_polygonize": {
            "post": {
                "tags": ["(rpc) st_polygonize"],
                "summary": "args: geomfield - Aggregate. Creates a GeometryCollection containing possible polygons formed from the constituent linework of a set of geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomfield - Aggregate. Creates a GeometryCollection containing possible polygons formed from the constituent linework of a set of geometries.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_z": {
            "post": {
                "tags": ["(rpc) st_z"],
                "summary": "args: a_point - Return the Z coordinate of the point, or NULL if not available. Input must be a point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_point - Return the Z coordinate of the point, or NULL if not available. Input must be a point.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_lengthspheroid": {
            "post": {
                "tags": ["(rpc) st_lengthspheroid"],
                "summary": "args: a_geometry, a_spheroid - Calculates the 2D or 3D length/perimeter of a geometry on an ellipsoid. This is useful if the coordinates of the geometry are in longitude/latitude and a length is desired without reprojection.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_geometry, a_spheroid - Calculates the 2D or 3D length/perimeter of a geometry on an ellipsoid. This is useful if the coordinates of the geometry are in longitude/latitude and a length is desired without reprojection.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_collect_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_collect_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box3d_in": {
            "post": {
                "tags": ["(rpc) box3d_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_coverage_tile": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_coverage_tile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setvalues": {
            "post": {
                "tags": ["(rpc) st_setvalues"],
                "summary": "args: rast, nband, columnx, rowy, width, height, newvalue, keepnodata=FALSE - Returns modified raster resulting from setting the values of a given band.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast",
                                "nband",
                                "x",
                                "y",
                                "width",
                                "height",
                                "newvalue",
                            ],
                            "type": "object",
                            "description": "args: rast, nband, columnx, rowy, width, height, newvalue, keepnodata=FALSE - Returns modified raster resulting from setting the values of a given band.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "height": {"format": "integer", "type": "integer"},
                                "nband": {"format": "integer", "type": "integer"},
                                "keepnodata": {"format": "boolean", "type": "boolean"},
                                "width": {"format": "integer", "type": "integer"},
                                "newvalue": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "x": {"format": "integer", "type": "integer"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gidx_in": {
            "post": {
                "tags": ["(rpc) gidx_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_overright": {
            "post": {
                "tags": ["(rpc) raster_overright"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_closestpointofapproach": {
            "post": {
                "tags": ["(rpc) st_closestpointofapproach"],
                "summary": "args: track1, track2 - Returns the measure at which points interpolated along two lines are closest.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: track1, track2 - Returns the measure at which points interpolated along two lines are closest.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_slope4ma": {
            "post": {
                "tags": ["(rpc) _st_slope4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_coverage_tile": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_coverage_tile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_unaryunion": {
            "post": {
                "tags": ["(rpc) st_unaryunion"],
                "summary": "args: geom - Like ST_Union, but working at the geometry component level.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom - Like ST_Union, but working at the geometry component level.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_hasarc": {
            "post": {
                "tags": ["(rpc) st_hasarc"],
                "summary": "args: geomA - Returns true if a geometry or geometry collection contains a circular string",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometry"],
                            "type": "object",
                            "description": "args: geomA - Returns true if a geometry or geometry collection contains a circular string",
                            "properties": {
                                "geometry": {"format": "geometry", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mapalgebra": {
            "post": {
                "tags": ["(rpc) st_mapalgebra"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "nband1",
                                "rast2",
                                "nband2",
                                "callbackfunc",
                            ],
                            "type": "object",
                            "properties": {
                                "callbackfunc": {
                                    "format": "regprocedure",
                                    "type": "string",
                                },
                                "distancey": {"format": "integer", "type": "integer"},
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "distancex": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                                "customextent": {"format": "raster", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                                "extenttype": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_type_name": {
            "post": {
                "tags": ["(rpc) postgis_type_name"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geomname", "coord_dimension"],
                            "type": "object",
                            "properties": {
                                "coord_dimension": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                                "geomname": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "use_new_name": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_offsetcurve": {
            "post": {
                "tags": ["(rpc) st_offsetcurve"],
                "summary": "args: line, signed_distance, style_parameters=' - Return an offset line at a given distance and side from an input line. Useful for computing parallel lines about a center line",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["line", "distance"],
                            "type": "object",
                            "description": "args: line, signed_distance, style_parameters=' - Return an offset line at a given distance and side from an input line. Useful for computing parallel lines about a center line",
                            "properties": {
                                "distance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "line": {"format": "geometry", "type": "string"},
                                "params": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_box2dfromgeohash": {
            "post": {
                "tags": ["(rpc) st_box2dfromgeohash"],
                "summary": "args: geohash, precision=full_precision_of_geohash - Return a BOX2D from a GeoHash string.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geohash, precision=full_precision_of_geohash - Return a BOX2D from a GeoHash string.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mpointfromtext": {
            "post": {
                "tags": ["(rpc) st_mpointfromtext"],
                "summary": "args: WKT, srid - Makes a Geometry from WKT with the given SRID. If SRID is not give, it defaults to 0.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Makes a Geometry from WKT with the given SRID. If SRID is not give, it defaults to 0.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_consistent_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_consistent_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box2d_out": {
            "post": {
                "tags": ["(rpc) box2d_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_geometry_overlap": {
            "post": {
                "tags": ["(rpc) raster_geometry_overlap"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_asx3d": {
            "post": {
                "tags": ["(rpc) _st_asx3d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dlength_spheroid": {
            "post": {
                "tags": ["(rpc) st_3dlength_spheroid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_typmod_srid": {
            "post": {
                "tags": ["(rpc) postgis_typmod_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_locatebetween": {
            "post": {
                "tags": ["(rpc) st_locatebetween"],
                "summary": "args: geomA, measure_start, measure_end, offset - Return a derived geometry collection value with elements that match the specified range of measures inclusively. Polygonal elements are not supported.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometry", "frommeasure", "tomeasure"],
                            "type": "object",
                            "description": "args: geomA, measure_start, measure_end, offset - Return a derived geometry collection value with elements that match the specified range of measures inclusively. Polygonal elements are not supported.",
                            "properties": {
                                "tomeasure": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "geometry": {"format": "geometry", "type": "string"},
                                "leftrightoffset": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "frommeasure": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_out": {
            "post": {
                "tags": ["(rpc) raster_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dclosestpoint": {
            "post": {
                "tags": ["(rpc) st_3dclosestpoint"],
                "summary": "args: g1, g2 - Returns the 3-dimensional point on g1 that is closest to g2. This is the first point of the 3D shortest line.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 3-dimensional point on g1 that is closest to g2. This is the first point of the 3D shortest line.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_min4ma": {
            "post": {
                "tags": ["(rpc) st_min4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_split": {
            "post": {
                "tags": ["(rpc) st_split"],
                "summary": "args: input, blade - Returns a collection of geometries resulting by splitting a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: input, blade - Returns a collection of geometries resulting by splitting a geometry.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_coveredby": {
            "post": {
                "tags": ["(rpc) st_coveredby"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastA lie outside raster rastB.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastA lie outside raster rastB.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asewkt": {
            "post": {
                "tags": ["(rpc) st_asewkt"],
                "summary": "args: g1 - Return the Well-Known Text (WKT) representation of the geometry with SRID meta data.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the Well-Known Text (WKT) representation of the geometry with SRID meta data.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_below": {
            "post": {
                "tags": ["(rpc) raster_below"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_subdivide": {
            "post": {
                "tags": ["(rpc) st_subdivide"],
                "summary": "args: geom, max_vertices=256 - Returns a set of geometry where no geometry in the set has more than the specified number of vertices.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom, max_vertices=256 - Returns a set of geometry where no geometry in the set has more than the specified number of vertices.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "maxvertices": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mean4ma": {
            "post": {
                "tags": ["(rpc) st_mean4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_scale": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_scale"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastschema",
                                "rasttable",
                                "rastcolumn",
                                "axis",
                            ],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "axis": {"format": "character", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isvalidtrajectory": {
            "post": {
                "tags": ["(rpc) st_isvalidtrajectory"],
                "summary": "args: line - Returns true if the geometry is a valid trajectory.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: line - Returns true if the geometry is a valid trajectory.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_area": {
            "post": {
                "tags": ["(rpc) st_area"],
                "summary": "args: geog, use_spheroid=true - Returns the area of the surface if it is a Polygon or MultiPolygon. For geometry, a 2D Cartesian area is determined with units specified by the SRID. For geography, area is determined on a curved surface with units in square meters.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geog"],
                            "type": "object",
                            "description": "args: geog, use_spheroid=true - Returns the area of the surface if it is a Polygon or MultiPolygon. For geometry, a 2D Cartesian area is determined with units specified by the SRID. For geography, area is determined on a curved surface with units in square meters.",
                            "properties": {
                                "geog": {"format": "geography", "type": "string"},
                                "use_spheroid": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomcollfromtext": {
            "post": {
                "tags": ["(rpc) st_geomcollfromtext"],
                "summary": "args: WKT, srid - Makes a collection Geometry from collection WKT with the given SRID. If SRID is not give, it defaults to 0.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Makes a collection Geometry from collection WKT with the given SRID. If SRID is not give, it defaults to 0.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_union_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_union_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asgdalraster": {
            "post": {
                "tags": ["(rpc) st_asgdalraster"],
                "summary": "args: rast, format, options=NULL, srid=sameassource - Return the raster tile in the designated GDAL Raster format. Raster formats are one of those supported by your compiled library. Use ST_GDALRasters() to get a list of formats supported by your library.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "format"],
                            "type": "object",
                            "description": "args: rast, format, options=NULL, srid=sameassource - Return the raster tile in the designated GDAL Raster format. Raster formats are one of those supported by your compiled library. Use ST_GDALRasters() to get a list of formats supported by your library.",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "rast": {"format": "raster", "type": "string"},
                                "format": {"format": "text", "type": "string"},
                                "options": {"format": "text[]", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_range4ma": {
            "post": {
                "tags": ["(rpc) st_range4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_askml": {
            "post": {
                "tags": ["(rpc) _st_askml"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_crosses": {
            "post": {
                "tags": ["(rpc) _st_crosses"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_histogram": {
            "post": {
                "tags": ["(rpc) _st_histogram"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "max": {"format": "double precision", "type": "number"},
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "width": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "min": {"format": "double precision", "type": "number"},
                                "right": {"format": "boolean", "type": "boolean"},
                                "bins": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_astiff": {
            "post": {
                "tags": ["(rpc) st_astiff"],
                "summary": "args: rast, nbands, options, srid=sameassource - Return the raster selected bands as a single TIFF image (byte array). If no band is specified, then will try to use all bands.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nbands"],
                            "type": "object",
                            "description": "args: rast, nbands, options, srid=sameassource - Return the raster selected bands as a single TIFF image (byte array). If no band is specified, then will try to use all bands.",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "rast": {"format": "raster", "type": "string"},
                                "nbands": {"format": "integer[]", "type": "string"},
                                "options": {"format": "text[]", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mpolyfromwkb": {
            "post": {
                "tags": ["(rpc) st_mpolyfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isempty": {
            "post": {
                "tags": ["(rpc) st_isempty"],
                "summary": "args: rast - Returns true if the raster is empty (width = 0 and height = 0). Otherwise, returns false.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast - Returns true if the raster is empty (width = 0 and height = 0). Otherwise, returns false.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelheight": {
            "post": {
                "tags": ["(rpc) st_pixelheight"],
                "summary": "args: rast - Returns the pixel height in geometric units of the spatial reference system.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the pixel height in geometric units of the spatial reference system.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_cleangeometry": {
            "post": {
                "tags": ["(rpc) st_cleangeometry"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_left": {
            "post": {
                "tags": ["(rpc) raster_left"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_scale": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_scale"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastschema",
                                "rasttable",
                                "rastcolumn",
                                "axis",
                            ],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "axis": {"format": "character", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_valuecount": {
            "post": {
                "tags": ["(rpc) _st_valuecount"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "rastertable": {"format": "text", "type": "string"},
                                "roundto": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                                "searchvalues": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_nodata_values": {
            "post": {
                "tags": ["(rpc) _raster_constraint_nodata_values"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_lt": {
            "post": {
                "tags": ["(rpc) geography_lt"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_buffer": {
            "post": {
                "tags": ["(rpc) _st_buffer"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/array_to_json_with_key": {
            "post": {
                "tags": ["(rpc) array_to_json_with_key"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_sharedpaths": {
            "post": {
                "tags": ["(rpc) st_sharedpaths"],
                "summary": "args: lineal1, lineal2 - Returns a collection containing paths shared by the two input linestrings/multilinestrings.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: lineal1, lineal2 - Returns a collection containing paths shared by the two input linestrings/multilinestrings.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_points": {
            "post": {
                "tags": ["(rpc) st_points"],
                "summary": "args: geom - Returns a MultiPoint containing all of the coordinates of a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom - Returns a MultiPoint containing all of the coordinates of a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/updategeometrysrid": {
            "post": {
                "tags": ["(rpc) updategeometrysrid"],
                "summary": "args: catalog_name, schema_name, table_name, column_name, srid - Updates the SRID of all features in a geometry column, geometry_columns metadata and srid. If it was enforced with constraints, the constraints will be updated with new srid constraint. If the old was enforced by type definition, the type definition will be changed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "catalogn_name",
                                "schema_name",
                                "table_name",
                                "column_name",
                                "new_srid_in",
                            ],
                            "type": "object",
                            "description": "args: catalog_name, schema_name, table_name, column_name, srid - Updates the SRID of all features in a geometry column, geometry_columns metadata and srid. If it was enforced with constraints, the constraints will be updated with new srid constraint. If the old was enforced by type definition, the type definition will be changed.",
                            "properties": {
                                "new_srid_in": {"format": "integer", "type": "integer"},
                                "catalogn_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "table_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "column_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "schema_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_summarystats_transfn": {
            "post": {
                "tags": ["(rpc) _st_summarystats_transfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_union_finalfn": {
            "post": {
                "tags": ["(rpc) _st_union_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_approxcount": {
            "post": {
                "tags": ["(rpc) st_approxcount"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_typmod_out": {
            "post": {
                "tags": ["(rpc) geometry_typmod_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/__st_countagg_transfn": {
            "post": {
                "tags": ["(rpc) __st_countagg_transfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["agg", "rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "agg": {"format": "agg_count", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_hasbbox": {
            "post": {
                "tags": ["(rpc) postgis_hasbbox"],
                "summary": "args: geomA - Returns TRUE if the bbox of this geometry is cached, FALSE otherwise.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns TRUE if the bbox of this geometry is cached, FALSE otherwise.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_distanceuncached": {
            "post": {
                "tags": ["(rpc) _st_distanceuncached"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geohash": {
            "post": {
                "tags": ["(rpc) st_geohash"],
                "summary": "args: geom, maxchars=full_precision_of_point - Return a GeoHash representation of the geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom, maxchars=full_precision_of_point - Return a GeoHash representation of the geometry.",
                            "properties": {
                                "maxchars": {"format": "integer", "type": "integer"},
                                "geom": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_clusterwithin": {
            "post": {
                "tags": ["(rpc) st_clusterwithin"],
                "summary": "args: g, distance - Aggregate. Returns an array of GeometryCollections, where each GeometryCollection represents a set of geometries separated by no more than the specified distance.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: g, distance - Aggregate. Returns an array of GeometryCollections, where each GeometryCollection represents a set of geometries separated by no more than the specified distance.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_worldtorastercoordx": {
            "post": {
                "tags": ["(rpc) st_worldtorastercoordx"],
                "summary": "args: rast, xw, yw - Returns the column in the raster of the point geometry (pt) or a X and Y world coordinate (xw, yw) represented in world spatial reference system of raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "xw", "yw"],
                            "type": "object",
                            "description": "args: rast, xw, yw - Returns the column in the raster of the point geometry (pt) or a X and Y world coordinate (xw, yw) represented in world spatial reference system of raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "xw": {"format": "double precision", "type": "number"},
                                "yw": {"format": "double precision", "type": "number"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enermaps_get_parameters": {
            "post": {
                "tags": ["(rpc) enermaps_get_parameters"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["id"],
                            "type": "object",
                            "properties": {
                                "id": {"format": "integer", "type": "integer"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rescale": {
            "post": {
                "tags": ["(rpc) st_rescale"],
                "summary": "args: rast, scalex, scaley, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster by adjusting only its scale (or pixel size). New pixel values are computed using the NearestNeighbor (english or american spelling), Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "scalex", "scaley"],
                            "type": "object",
                            "description": "args: rast, scalex, scaley, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster by adjusting only its scale (or pixel size). New pixel values are computed using the NearestNeighbor (english or american spelling), Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "algorithm": {"format": "text", "type": "string"},
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_out_db": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_out_db"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_height": {
            "post": {
                "tags": ["(rpc) st_height"],
                "summary": "args: rast - Returns the height of the raster in pixels.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the height of the raster in pixels.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_astext": {
            "post": {
                "tags": ["(rpc) st_astext"],
                "summary": "args: g1 - Return the Well-Known Text (WKT) representation of the geometry/geography without SRID metadata.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the Well-Known Text (WKT) representation of the geometry/geography without SRID metadata.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asgeojson": {
            "post": {
                "tags": ["(rpc) st_asgeojson"],
                "summary": "args: gj_version, geom, maxdecimaldigits=15, options=0 - Return the geometry as a GeoJSON element.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["gj_version", "geom"],
                            "type": "object",
                            "description": "args: gj_version, geom, maxdecimaldigits=15, options=0 - Return the geometry as a GeoJSON element.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "gj_version": {"format": "integer", "type": "integer"},
                                "options": {"format": "integer", "type": "integer"},
                                "maxdecimaldigits": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mem_size": {
            "post": {
                "tags": ["(rpc) st_mem_size"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_tri": {
            "post": {
                "tags": ["(rpc) st_tri"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "customextent"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "customextent": {"format": "raster", "type": "string"},
                                "interpolate_nodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linesubstring": {
            "post": {
                "tags": ["(rpc) st_linesubstring"],
                "summary": "args: a_linestring, startfraction, endfraction - Return a linestring being a substring of the input one starting and ending at the given fractions of total 2d length. Second and third arguments are float8 values between 0 and 1.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double"],
                            "type": "object",
                            "description": "args: a_linestring, startfraction, endfraction - Return a linestring being a substring of the input one starting and ending at the given fractions of total 2d length. Second and third arguments are float8 values between 0 and 1.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rastertoworldcoordx": {
            "post": {
                "tags": ["(rpc) st_rastertoworldcoordx"],
                "summary": "args: rast, xcolumn, yrow - Returns the geometric X coordinate upper left of a raster, column and row. Numbering of columns and rows starts at 1.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "xr", "yr"],
                            "type": "object",
                            "description": "args: rast, xcolumn, yrow - Returns the geometric X coordinate upper left of a raster, column and row. Numbering of columns and rows starts at 1.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "xr": {"format": "integer", "type": "integer"},
                                "yr": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_clusterintersecting": {
            "post": {
                "tags": ["(rpc) st_clusterintersecting"],
                "summary": "args: g - Aggregate. Returns an array with the connected components of a set of geometries",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Aggregate. Returns an array with the connected components of a set of geometries",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_overview_constraint": {
            "post": {
                "tags": ["(rpc) _add_overview_constraint"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "ovschema",
                                "ovtable",
                                "ovcolumn",
                                "refschema",
                                "reftable",
                                "refcolumn",
                                "factor",
                            ],
                            "type": "object",
                            "properties": {
                                "ovcolumn": {"format": "name", "type": "string"},
                                "reftable": {"format": "name", "type": "string"},
                                "factor": {"format": "integer", "type": "integer"},
                                "ovschema": {"format": "name", "type": "string"},
                                "ovtable": {"format": "name", "type": "string"},
                                "refcolumn": {"format": "name", "type": "string"},
                                "refschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography": {
            "post": {
                "tags": ["(rpc) geography"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_version": {
            "post": {
                "tags": ["(rpc) postgis_version"],
                "summary": "Returns PostGIS version number and compile-time options.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns PostGIS version number and compile-time options.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setbandisnodata": {
            "post": {
                "tags": ["(rpc) st_setbandisnodata"],
                "summary": "args: rast, band=1 - Sets the isnodata flag of the band to TRUE.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, band=1 - Sets the isnodata flag of the band to TRUE.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force3dz": {
            "post": {
                "tags": ["(rpc) st_force3dz"],
                "summary": "args: geomA - Force the geometries into XYZ mode.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Force the geometries into XYZ mode.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_maxdistance": {
            "post": {
                "tags": ["(rpc) _st_maxdistance"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enermaps_set_legend": {
            "post": {
                "tags": ["(rpc) enermaps_set_legend"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["parameters", "legend"],
                            "type": "object",
                            "properties": {
                                "parameters": {"format": "text", "type": "string"},
                                "legend": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_distance_knn": {
            "post": {
                "tags": ["(rpc) geography_distance_knn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_minimumclearanceline": {
            "post": {
                "tags": ["(rpc) st_minimumclearanceline"],
                "summary": "args: g - Returns the two-point LineString spanning a geometrys minimum clearance.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Returns the two-point LineString spanning a geometrys minimum clearance.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_buffer": {
            "post": {
                "tags": ["(rpc) st_buffer"],
                "summary": "args: g1, radius_of_buffer_in_meters - (T)Returns a geometry covering all points within a given distancefrom the input geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: g1, radius_of_buffer_in_meters - (T)Returns a geometry covering all points within a given distancefrom the input geometry.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_scalex": {
            "post": {
                "tags": ["(rpc) st_scalex"],
                "summary": "args: rast - Returns the X component of the pixel width in units of coordinate reference system.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the X component of the pixel width in units of coordinate reference system.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force_3dm": {
            "post": {
                "tags": ["(rpc) st_force_3dm"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dimension": {
            "post": {
                "tags": ["(rpc) st_dimension"],
                "summary": "args: g - The inherent dimension of this Geometry object, which must be less than or equal to the coordinate dimension.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - The inherent dimension of this Geometry object, which must be less than or equal to the coordinate dimension.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_overbelow": {
            "post": {
                "tags": ["(rpc) geometry_overbelow"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromgml": {
            "post": {
                "tags": ["(rpc) st_geomfromgml"],
                "summary": "args: geomgml, srid - Takes as input GML representation of geometry and outputs a PostGIS geometry object",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomgml, srid - Takes as input GML representation of geometry and outputs a PostGIS geometry object",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_valuepercent": {
            "post": {
                "tags": ["(rpc) st_valuepercent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastertable",
                                "rastercolumn",
                                "nband",
                                "exclude_nodata_value",
                                "searchvalue",
                            ],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "searchvalue": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "roundto": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dmaxdistance": {
            "post": {
                "tags": ["(rpc) st_3dmaxdistance"],
                "summary": "args: g1, g2 - For geometry type Returns the 3-dimensional cartesian maximum distance (based on spatial ref) between two geometries in projected units.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - For geometry type Returns the 3-dimensional cartesian maximum distance (based on spatial ref) between two geometries in projected units.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_tri4ma": {
            "post": {
                "tags": ["(rpc) _st_tri4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_astwkb": {
            "post": {
                "tags": ["(rpc) st_astwkb"],
                "summary": 'args: geometries, unique_ids, decimaldigits_xy=0, decimaldigits_z=0, decimaldigits_m=0, include_sizes=false, include_bounding_boxes=false - Returns the geometry as TWKB, aka "Tiny Well-Known Binary"',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "ids"],
                            "type": "object",
                            "description": 'args: geometries, unique_ids, decimaldigits_xy=0, decimaldigits_z=0, decimaldigits_m=0, include_sizes=false, include_bounding_boxes=false - Returns the geometry as TWKB, aka "Tiny Well-Known Binary"',
                            "properties": {
                                "prec": {"format": "integer", "type": "integer"},
                                "geom": {"format": "geometry[]", "type": "string"},
                                "with_sizes": {"format": "boolean", "type": "boolean"},
                                "ids": {"format": "bigint[]", "type": "string"},
                                "with_boxes": {"format": "boolean", "type": "boolean"},
                                "prec_z": {"format": "integer", "type": "integer"},
                                "prec_m": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mlinefromtext": {
            "post": {
                "tags": ["(rpc) st_mlinefromtext"],
                "summary": "args: WKT, srid - Return a specified ST_MultiLineString value from WKT representation.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Return a specified ST_MultiLineString value from WKT representation.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_line_substring": {
            "post": {
                "tags": ["(rpc) st_line_substring"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_disjoint": {
            "post": {
                "tags": ["(rpc) st_disjoint"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA does not spatially intersect rastB.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA does not spatially intersect rastB.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_iscoveragetile": {
            "post": {
                "tags": ["(rpc) st_iscoveragetile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "coverage", "tilewidth", "tileheight"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "tilewidth": {"format": "integer", "type": "integer"},
                                "coverage": {"format": "raster", "type": "string"},
                                "tileheight": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_out_db": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_out_db"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isvalidreason": {
            "post": {
                "tags": ["(rpc) st_isvalidreason"],
                "summary": "args: geomA, flags - Returns text stating if a geometry is valid or not and if not valid, a reason why.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA, flags - Returns text stating if a geometry is valid or not and if not valid, a reason why.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isclosed": {
            "post": {
                "tags": ["(rpc) st_isclosed"],
                "summary": "args: g - Returns TRUE if the LINESTRINGs start and end points are coincident. For Polyhedral surface is closed (volumetric).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Returns TRUE if the LINESTRINGs start and end points are coincident. For Polyhedral surface is closed (volumetric).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_alignment": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_alignment"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setskew": {
            "post": {
                "tags": ["(rpc) st_setskew"],
                "summary": "args: rast, skewx, skewy - Sets the georeference X and Y skew (or rotation parameter). If only one is passed in, sets X and Y to the same value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "skewx", "skewy"],
                            "type": "object",
                            "description": "args: rast, skewx, skewy - Sets the georeference X and Y skew (or rotation parameter). If only one is passed in, sets X and Y to the same value.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_symdifference": {
            "post": {
                "tags": ["(rpc) st_symdifference"],
                "summary": "args: geomA, geomB - Returns a geometry that represents the portions of A and B that do not intersect. It is called a symmetric difference because ST_SymDifference(A,B) = ST_SymDifference(B,A).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: geomA, geomB - Returns a geometry that represents the portions of A and B that do not intersect. It is called a symmetric difference because ST_SymDifference(A,B) = ST_SymDifference(B,A).",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/get_proj4_from_srid": {
            "post": {
                "tags": ["(rpc) get_proj4_from_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_overview_constraint": {
            "post": {
                "tags": ["(rpc) _drop_overview_constraint"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["ovschema", "ovtable", "ovcolumn"],
                            "type": "object",
                            "properties": {
                                "ovcolumn": {"format": "name", "type": "string"},
                                "ovschema": {"format": "name", "type": "string"},
                                "ovtable": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_seteffectivearea": {
            "post": {
                "tags": ["(rpc) st_seteffectivearea"],
                "summary": "args: geomA, threshold = 0, set_area = 1 - Sets the effective area for each vertex, storing the value in the M ordinate. A simplified geometry can then be generated by filtering on the M ordinate.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA, threshold = 0, set_area = 1 - Sets the effective area for each vertex, storing the value in the M ordinate. A simplified geometry can then be generated by filtering on the M ordinate.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_memsize": {
            "post": {
                "tags": ["(rpc) st_memsize"],
                "summary": "args: rast - Returns the amount of space (in bytes) the raster takes.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the amount of space (in bytes) the raster takes.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_same_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_same_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_zmin": {
            "post": {
                "tags": ["(rpc) st_zmin"],
                "summary": "args: aGeomorBox2DorBox3D - Returns Z minima of a bounding box 2d or 3d or a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aGeomorBox2DorBox3D - Returns Z minima of a bounding box 2d or 3d or a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_valuecount": {
            "post": {
                "tags": ["(rpc) st_valuecount"],
                "summary": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true, searchvalues=NULL, roundto=0, OUT value, OUT count - Returns a set of records containing a pixel band value and count of the number of pixels in a given band of a raster (or a raster coverage) that have a given set of values. If no band is specified defaults to band 1. By default nodata value pixels are not counted. and all other values in the pixel are output and pixel band values are rounded to the nearest integer.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "description": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true, searchvalues=NULL, roundto=0, OUT value, OUT count - Returns a set of records containing a pixel band value and count of the number of pixels in a given band of a raster (or a raster coverage) that have a given set of values. If no band is specified defaults to band 1. By default nodata value pixels are not counted. and all other values in the pixel are output and pixel band values are rounded to the nearest integer.",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "rastertable": {"format": "text", "type": "string"},
                                "roundto": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                                "searchvalues": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_exteriorring": {
            "post": {
                "tags": ["(rpc) st_exteriorring"],
                "summary": "args: a_polygon - Returns a line string representing the exterior ring of the POLYGON geometry. Return NULL if the geometry is not a polygon. Will not work with MULTIPOLYGON",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_polygon - Returns a line string representing the exterior ring of the POLYGON geometry. Return NULL if the geometry is not a polygon. Will not work with MULTIPOLYGON",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_proj_version": {
            "post": {
                "tags": ["(rpc) postgis_proj_version"],
                "summary": "Returns the version number of the PROJ4 library.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns the version number of the PROJ4 library.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_scale": {
            "post": {
                "tags": ["(rpc) st_scale"],
                "summary": "args: geomA, XFactor, YFactor, ZFactor - Scale a geometry by given factors.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double"],
                            "type": "object",
                            "description": "args: geomA, XFactor, YFactor, ZFactor - Scale a geometry by given factors.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_alignment": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_alignment"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_relatematch": {
            "post": {
                "tags": ["(rpc) st_relatematch"],
                "summary": "args: intersectionMatrix, intersectionMatrixPattern - Returns true if intersectionMattrixPattern1 implies intersectionMatrixPattern2",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: intersectionMatrix, intersectionMatrixPattern - Returns true if intersectionMattrixPattern1 implies intersectionMatrixPattern2",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_out_db": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_out_db"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_contained": {
            "post": {
                "tags": ["(rpc) raster_contained"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_penalty_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_penalty_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_dumprings": {
            "post": {
                "tags": ["(rpc) st_dumprings"],
                "summary": "args: a_polygon - Returns a set of geometry_dump rows, representing the exterior and interior rings of a polygon.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_polygon - Returns a set of geometry_dump rows, representing the exterior and interior rings of a polygon.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_distance_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_distance_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_coorddim": {
            "post": {
                "tags": ["(rpc) st_coorddim"],
                "summary": "args: geomA - Return the coordinate dimension of the ST_Geometry value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometry"],
                            "type": "object",
                            "description": "args: geomA - Return the coordinate dimension of the ST_Geometry value.",
                            "properties": {
                                "geometry": {"format": "geometry", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_picksplit_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_picksplit_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_ymax": {
            "post": {
                "tags": ["(rpc) st_ymax"],
                "summary": "args: aGeomorBox2DorBox3D - Returns Y maxima of a bounding box 2d or 3d or a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aGeomorBox2DorBox3D - Returns Y maxima of a bounding box 2d or 3d or a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_hillshade4ma": {
            "post": {
                "tags": ["(rpc) _st_hillshade4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_segmentize": {
            "post": {
                "tags": ["(rpc) st_segmentize"],
                "summary": "args: geog, max_segment_length - Return a modified geometry/geography having no segment longer than the given distance.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geog", "max_segment_length"],
                            "type": "object",
                            "description": "args: geog, max_segment_length - Return a modified geometry/geography having no segment longer than the given distance.",
                            "properties": {
                                "geog": {"format": "geography", "type": "string"},
                                "max_segment_length": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelaspoints": {
            "post": {
                "tags": ["(rpc) st_pixelaspoints"],
                "summary": "args: rast, band=1, exclude_nodata_value=TRUE - Returns a point geometry for each pixel of a raster band along with the value, the X and the Y raster coordinates of each pixel. The coordinates of the point geometry are of the pixels upper-left corner.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, band=1, exclude_nodata_value=TRUE - Returns a point geometry for each pixel of a raster band along with the value, the X and the Y raster coordinates of each pixel. The coordinates of the point geometry are of the pixels upper-left corner.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_slope": {
            "post": {
                "tags": ["(rpc) st_slope"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "customextent"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "scale": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "pixeltype": {"format": "text", "type": "string"},
                                "units": {"format": "text", "type": "string"},
                                "customextent": {"format": "raster", "type": "string"},
                                "interpolate_nodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_gdalwarp": {
            "post": {
                "tags": ["(rpc) _st_gdalwarp"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "srid": {"format": "integer", "type": "integer"},
                                "rast": {"format": "raster", "type": "string"},
                                "height": {"format": "integer", "type": "integer"},
                                "gridx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "gridy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "algorithm": {"format": "text", "type": "string"},
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_dwithinuncached": {
            "post": {
                "tags": ["(rpc) _st_dwithinuncached"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_normalize": {
            "post": {
                "tags": ["(rpc) st_normalize"],
                "summary": "args: geom - Return the geometry in its canonical form.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom - Return the geometry in its canonical form.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_summarystats": {
            "post": {
                "tags": ["(rpc) st_summarystats"],
                "summary": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true - Returns summarystats consisting of count, sum, mean, stddev, min, max for a given raster band of a raster or raster coverage. Band 1 is assumed is no band is specified.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "description": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true - Returns summarystats consisting of count, sum, mean, stddev, min, max for a given raster band of a raster or raster coverage. Band 1 is assumed is no band is specified.",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/overlaps_nd": {
            "post": {
                "tags": ["(rpc) overlaps_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_ndims": {
            "post": {
                "tags": ["(rpc) st_ndims"],
                "summary": "args: g1 - Returns coordinate dimension of the geometry as a small int. Values are: 2,3 or 4.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Returns coordinate dimension of the geometry as a small int. Values are: 2,3 or 4.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linefromtext": {
            "post": {
                "tags": ["(rpc) st_linefromtext"],
                "summary": "args: WKT, srid - Makes a Geometry from WKT representation with the given SRID. If SRID is not given, it defaults to 0.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Makes a Geometry from WKT representation with the given SRID. If SRID is not given, it defaults to 0.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/addgeometrycolumn": {
            "post": {
                "tags": ["(rpc) addgeometrycolumn"],
                "summary": "args: catalog_name, schema_name, table_name, column_name, srid, type, dimension, use_typmod=true - Adds a geometry column to an existing table of attributes. By default uses type modifier to define rather than constraints. Pass in false for use_typmod to get old check constraint based behavior",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "catalog_name",
                                "schema_name",
                                "table_name",
                                "column_name",
                                "new_srid_in",
                                "new_type",
                                "new_dim",
                            ],
                            "type": "object",
                            "description": "args: catalog_name, schema_name, table_name, column_name, srid, type, dimension, use_typmod=true - Adds a geometry column to an existing table of attributes. By default uses type modifier to define rather than constraints. Pass in false for use_typmod to get old check constraint based behavior",
                            "properties": {
                                "new_dim": {"format": "integer", "type": "integer"},
                                "new_srid_in": {"format": "integer", "type": "integer"},
                                "use_typmod": {"format": "boolean", "type": "boolean"},
                                "catalog_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "new_type": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "table_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "column_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                                "schema_name": {
                                    "format": "character varying",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_lineinterpolatepoint": {
            "post": {
                "tags": ["(rpc) st_lineinterpolatepoint"],
                "summary": "args: a_linestring, a_fraction - Returns a point interpolated along a line. Second argument is a float8 between 0 and 1 representing fraction of total length of linestring the point has to be located.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: a_linestring, a_fraction - Returns a point interpolated along a line. Second argument is a float8 between 0 and 1 representing fraction of total length of linestring the point has to be located.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_addpoint": {
            "post": {
                "tags": ["(rpc) st_addpoint"],
                "summary": "args: linestring, point, position - Add a point to a LineString.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: linestring, point, position - Add a point to a LineString.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_samealignment": {
            "post": {
                "tags": ["(rpc) st_samealignment"],
                "summary": "args: ulx1, uly1, scalex1, scaley1, skewx1, skewy1, ulx2, uly2, scalex2, scaley2, skewx2, skewy2 - Returns true if rasters have same skew, scale, spatial ref, and offset (pixels can be put on same grid without cutting into pixels) and false if they dont with notice detailing issue.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "ulx1",
                                "uly1",
                                "scalex1",
                                "scaley1",
                                "skewx1",
                                "skewy1",
                                "ulx2",
                                "uly2",
                                "scalex2",
                                "scaley2",
                                "skewx2",
                                "skewy2",
                            ],
                            "type": "object",
                            "description": "args: ulx1, uly1, scalex1, scaley1, skewx1, skewy1, ulx2, uly2, scalex2, scaley2, skewx2, skewy2 - Returns true if rasters have same skew, scale, spatial ref, and offset (pixels can be put on same grid without cutting into pixels) and false if they dont with notice detailing issue.",
                            "properties": {
                                "skewy1": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scalex2": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewx2": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley1": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "ulx2": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "uly1": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "uly2": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "ulx1": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewx1": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley2": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scalex1": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy2": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_perimeter": {
            "post": {
                "tags": ["(rpc) st_perimeter"],
                "summary": "args: geog, use_spheroid=true - Return the length measurement of the boundary of an ST_Surface or ST_MultiSurface geometry or geography. (Polygon, MultiPolygon). geometry measurement is in units of spatial reference and geography is in meters.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geog"],
                            "type": "object",
                            "description": "args: geog, use_spheroid=true - Return the length measurement of the boundary of an ST_Surface or ST_MultiSurface geometry or geography. (Polygon, MultiPolygon). geometry measurement is in units of spatial reference and geography is in meters.",
                            "properties": {
                                "geog": {"format": "geography", "type": "string"},
                                "use_spheroid": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_hausdorffdistance": {
            "post": {
                "tags": ["(rpc) st_hausdorffdistance"],
                "summary": "args: g1, g2, densifyFrac - Returns the Hausdorff distance between two geometries. Basically a measure of how similar or dissimilar 2 geometries are. Units are in the units of the spatial reference system of the geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2", "double"],
                            "type": "object",
                            "description": "args: g1, g2, densifyFrac - Returns the Hausdorff distance between two geometries. Basically a measure of how similar or dissimilar 2 geometries are. Units are in the units of the spatial reference system of the geometries.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"},
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_forcerhr": {
            "post": {
                "tags": ["(rpc) st_forcerhr"],
                "summary": "args: g - Force the orientation of the vertices in a polygon to follow the Right-Hand-Rule.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Force the orientation of the vertices in a polygon to follow the Right-Hand-Rule.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_reskew": {
            "post": {
                "tags": ["(rpc) st_reskew"],
                "summary": "args: rast, skewx, skewy, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster by adjusting only its skew (or rotation parameters). New pixel values are computed using the NearestNeighbor (english or american spelling), Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "skewx", "skewy"],
                            "type": "object",
                            "description": "args: rast, skewx, skewy, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster by adjusting only its skew (or rotation parameters). New pixel values are computed using the NearestNeighbor (english or american spelling), Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "algorithm": {"format": "text", "type": "string"},
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelascentroids": {
            "post": {
                "tags": ["(rpc) st_pixelascentroids"],
                "summary": "args: rast, band=1, exclude_nodata_value=TRUE - Returns the centroid (point geometry) for each pixel of a raster band along with the value, the X and the Y raster coordinates of each pixel. The point geometry is the centroid of the area represented by a pixel.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, band=1, exclude_nodata_value=TRUE - Returns the centroid (point geometry) for each pixel of a raster band along with the value, the X and the Y raster coordinates of each pixel. The point geometry is the centroid of the area represented by a pixel.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_closestpoint": {
            "post": {
                "tags": ["(rpc) st_closestpoint"],
                "summary": "args: g1, g2 - Returns the 2-dimensional point on g1 that is closest to g2. This is the first point of the shortest line.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 2-dimensional point on g1 that is closest to g2. This is the first point of the shortest line.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linecrossingdirection": {
            "post": {
                "tags": ["(rpc) st_linecrossingdirection"],
                "summary": "args: linestringA, linestringB - Given 2 linestrings, returns a number between -3 and 3 denoting what kind of crossing behavior. 0 is no crossing.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: linestringA, linestringB - Given 2 linestrings, returns a number between -3 and 3 denoting what kind of crossing behavior. 0 is no crossing.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/path": {
            "post": {
                "tags": ["(rpc) path"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_clusterkmeans": {
            "post": {
                "tags": ["(rpc) st_clusterkmeans"],
                "summary": "args: geom, number_of_clusters - Windowing function that returns integer id for the cluster each input geometry is in.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "k"],
                            "type": "object",
                            "description": "args: geom, number_of_clusters - Windowing function that returns integer id for the cluster each input geometry is in.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "k": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linefrommultipoint": {
            "post": {
                "tags": ["(rpc) st_linefrommultipoint"],
                "summary": "args: aMultiPoint - Creates a LineString from a MultiPoint geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aMultiPoint - Creates a LineString from a MultiPoint geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/text": {
            "post": {
                "tags": ["(rpc) text"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_lt": {
            "post": {
                "tags": ["(rpc) geometry_lt"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_simplify": {
            "post": {
                "tags": ["(rpc) st_simplify"],
                "summary": 'args: geomA, tolerance, preserveCollapsed - Returns a "simplified" version of the given geometry using the Douglas-Peucker algorithm.',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": 'args: geomA, tolerance, preserveCollapsed - Returns a "simplified" version of the given geometry using the Douglas-Peucker algorithm.',
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_mapalgebra": {
            "post": {
                "tags": ["(rpc) _st_mapalgebra"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastbandargset", "callbackfunc"],
                            "type": "object",
                            "properties": {
                                "callbackfunc": {
                                    "format": "regprocedure",
                                    "type": "string",
                                },
                                "distancey": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "rastbandargset": {
                                    "format": "rastbandarg[]",
                                    "type": "string",
                                },
                                "distancex": {"format": "integer", "type": "integer"},
                                "mask": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "customextent": {"format": "raster", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                                "extenttype": {"format": "text", "type": "string"},
                                "weighted": {"format": "boolean", "type": "boolean"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/is_contained_2d": {
            "post": {
                "tags": ["(rpc) is_contained_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enermaps_get_rasters": {
            "post": {
                "tags": ["(rpc) enermaps_get_rasters"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["parameters"],
                            "type": "object",
                            "properties": {
                                "parameters": {"format": "text", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_typmod_out": {
            "post": {
                "tags": ["(rpc) geography_typmod_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_union_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_union_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelaspolygons": {
            "post": {
                "tags": ["(rpc) st_pixelaspolygons"],
                "summary": "args: rast, band=1, exclude_nodata_value=TRUE - Returns the polygon geometry that bounds every pixel of a raster band along with the value, the X and the Y raster coordinates of each pixel.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, band=1, exclude_nodata_value=TRUE - Returns the polygon geometry that bounds every pixel of a raster band along with the value, the X and the Y raster coordinates of each pixel.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_right": {
            "post": {
                "tags": ["(rpc) geometry_right"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/overlaps_geog": {
            "post": {
                "tags": ["(rpc) overlaps_geog"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_minimumboundingcircle": {
            "post": {
                "tags": ["(rpc) st_minimumboundingcircle"],
                "summary": "args: geomA, num_segs_per_qt_circ=48 - Returns the smallest circle polygon that can fully contain a geometry. Default uses 48 segments per quarter circle.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["inputgeom"],
                            "type": "object",
                            "description": "args: geomA, num_segs_per_qt_circ=48 - Returns the smallest circle polygon that can fully contain a geometry. Default uses 48 segments per quarter circle.",
                            "properties": {
                                "inputgeom": {"format": "geometry", "type": "string"},
                                "segs_per_quarter": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_below": {
            "post": {
                "tags": ["(rpc) geometry_below"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_intersects": {
            "post": {
                "tags": ["(rpc) st_intersects"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA spatially intersects raster rastB.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA spatially intersects raster rastB.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_concavehull": {
            "post": {
                "tags": ["(rpc) st_concavehull"],
                "summary": "args: geomA, target_percent, allow_holes=false - The concave hull of a geometry represents a possibly concave geometry that encloses all geometries within the set. You can think of it as shrink wrapping.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["param_geom", "param_pctconvex"],
                            "type": "object",
                            "description": "args: geomA, target_percent, allow_holes=false - The concave hull of a geometry represents a possibly concave geometry that encloses all geometries within the set. You can think of it as shrink wrapping.",
                            "properties": {
                                "param_pctconvex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "param_geom": {"format": "geometry", "type": "string"},
                                "param_allow_holes": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_nodata_values": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_nodata_values"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/checkauth": {
            "post": {
                "tags": ["(rpc) checkauth"],
                "summary": "args: a_table_name, a_key_column_name - Creates trigger on a table to prevent/allow updates and deletes of rows based on authorization token.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_table_name, a_key_column_name - Creates trigger on a table to prevent/allow updates and deletes of rows based on authorization token.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_shortestline": {
            "post": {
                "tags": ["(rpc) st_shortestline"],
                "summary": "args: g1, g2 - Returns the 2-dimensional shortest line between two geometries",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 2-dimensional shortest line between two geometries",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_cache_bbox": {
            "post": {
                "tags": ["(rpc) postgis_cache_bbox"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_reclass": {
            "post": {
                "tags": ["(rpc) _st_reclass"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "VARIADIC"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "VARIADIC": {
                                    "format": "reclassargset reclassarg[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/find_srid": {
            "post": {
                "tags": ["(rpc) find_srid"],
                "summary": "args: a_schema_name, a_table_name, a_geomfield_name - The syntax is find_srid(a_db_schema, a_table, a_column) and the function returns the integer SRID of the specified column by searching through the GEOMETRY_COLUMNS table.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["character", "character", "character"],
                            "type": "object",
                            "description": "args: a_schema_name, a_table_name, a_geomfield_name - The syntax is find_srid(a_db_schema, a_table, a_column) and the function returns the integer SRID of the specified column by searching through the GEOMETRY_COLUMNS table.",
                            "properties": {
                                "character": {"format": "varying", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_zmax": {
            "post": {
                "tags": ["(rpc) st_zmax"],
                "summary": "args: aGeomorBox2DorBox3D - Returns Z minima of a bounding box 2d or 3d or a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aGeomorBox2DorBox3D - Returns Z minima of a bounding box 2d or 3d or a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_clip": {
            "post": {
                "tags": ["(rpc) st_clip"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "geom"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer[]", "type": "string"},
                                "nodataval": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "geom": {"format": "geometry", "type": "string"},
                                "crop": {"format": "boolean", "type": "boolean"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_neighborhood": {
            "post": {
                "tags": ["(rpc) st_neighborhood"],
                "summary": "args: rast, bandnum, columnX, rowY, distanceX, distanceY, exclude_nodata_value=true - Returns a 2-D double precision array of the non-NODATA values around a given bands pixel specified by either a columnX and rowY or a geometric point expressed in the same spatial reference coordinate system as the raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast",
                                "band",
                                "columnx",
                                "rowy",
                                "distancex",
                                "distancey",
                            ],
                            "type": "object",
                            "description": "args: rast, bandnum, columnX, rowY, distanceX, distanceY, exclude_nodata_value=true - Returns a 2-D double precision array of the non-NODATA values around a given bands pixel specified by either a columnX and rowY or a geometric point expressed in the same spatial reference coordinate system as the raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "distancey": {"format": "integer", "type": "integer"},
                                "rowy": {"format": "integer", "type": "integer"},
                                "distancex": {"format": "integer", "type": "integer"},
                                "columnx": {"format": "integer", "type": "integer"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_3dintersects": {
            "post": {
                "tags": ["(rpc) _st_3dintersects"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_postgis_selectivity": {
            "post": {
                "tags": ["(rpc) _postgis_selectivity"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["tbl", "att_name", "geom"],
                            "type": "object",
                            "properties": {
                                "tbl": {"format": "regclass", "type": "string"},
                                "geom": {"format": "geometry", "type": "string"},
                                "mode": {"format": "text", "type": "string"},
                                "att_name": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_worldtorastercoordy": {
            "post": {
                "tags": ["(rpc) st_worldtorastercoordy"],
                "summary": "args: rast, xw, yw - Returns the row in the raster of the point geometry (pt) or a X and Y world coordinate (xw, yw) represented in world spatial reference system of raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "xw", "yw"],
                            "type": "object",
                            "description": "args: rast, xw, yw - Returns the row in the raster of the point geometry (pt) or a X and Y world coordinate (xw, yw) represented in world spatial reference system of raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "xw": {"format": "double precision", "type": "number"},
                                "yw": {"format": "double precision", "type": "number"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelaspoint": {
            "post": {
                "tags": ["(rpc) st_pixelaspoint"],
                "summary": "args: rast, columnx, rowy - Returns a point geometry of the pixels upper-left corner.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "x", "y"],
                            "type": "object",
                            "description": "args: rast, columnx, rowy - Returns a point geometry of the pixels upper-left corner.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "x": {"format": "integer", "type": "integer"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_georeference": {
            "post": {
                "tags": ["(rpc) st_georeference"],
                "summary": "args: rast, format=GDAL - Returns the georeference meta data in GDAL or ESRI format as commonly seen in a world file. Default is GDAL.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, format=GDAL - Returns the georeference meta data in GDAL or ESRI format as commonly seen in a world file. Default is GDAL.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "format": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_typmod_type": {
            "post": {
                "tags": ["(rpc) postgis_typmod_type"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_extent": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_extent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_azimuth": {
            "post": {
                "tags": ["(rpc) st_azimuth"],
                "summary": "args: pointA, pointB - Returns the north-based azimuth as the angle in radians measured clockwise from the vertical on pointA to pointB.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: pointA, pointB - Returns the north-based azimuth as the angle in radians measured clockwise from the vertical on pointA to pointB.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/spheroid_in": {
            "post": {
                "tags": ["(rpc) spheroid_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_minimumclearance": {
            "post": {
                "tags": ["(rpc) st_minimumclearance"],
                "summary": "args: g - Returns the minimum clearance of a geometry, a measure of a geometrys robustness.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Returns the minimum clearance of a geometry, a measure of a geometrys robustness.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_contains": {
            "post": {
                "tags": ["(rpc) geometry_contains"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelwidth": {
            "post": {
                "tags": ["(rpc) st_pixelwidth"],
                "summary": "args: rast - Returns the pixel width in geometric units of the spatial reference system.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the pixel width in geometric units of the spatial reference system.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rastertoworldcoordy": {
            "post": {
                "tags": ["(rpc) st_rastertoworldcoordy"],
                "summary": "args: rast, xcolumn, yrow - Returns the geometric Y coordinate upper left corner of a raster, column and row. Numbering of columns and rows starts at 1.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "xr", "yr"],
                            "type": "object",
                            "description": "args: rast, xcolumn, yrow - Returns the geometric Y coordinate upper left corner of a raster, column and row. Numbering of columns and rows starts at 1.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "xr": {"format": "integer", "type": "integer"},
                                "yr": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelaspolygon": {
            "post": {
                "tags": ["(rpc) st_pixelaspolygon"],
                "summary": "args: rast, columnx, rowy - Returns the polygon geometry that bounds the pixel for a particular row and column.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "x", "y"],
                            "type": "object",
                            "description": "args: rast, columnx, rowy - Returns the polygon geometry that bounds the pixel for a particular row and column.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "x": {"format": "integer", "type": "integer"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_asraster": {
            "post": {
                "tags": ["(rpc) _st_asraster"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "properties": {
                                "touched": {"format": "boolean", "type": "boolean"},
                                "height": {"format": "integer", "type": "integer"},
                                "nodataval": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "geom": {"format": "geometry", "type": "string"},
                                "pixeltype": {"format": "text[]", "type": "string"},
                                "gridx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "upperlefty": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "gridy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "upperleftx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_width": {
            "post": {
                "tags": ["(rpc) st_width"],
                "summary": "args: rast - Returns the width of the raster in pixels.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the width of the raster in pixels.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_countagg_finalfn": {
            "post": {
                "tags": ["(rpc) _st_countagg_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["agg"],
                            "type": "object",
                            "properties": {
                                "agg": {"format": "agg_count", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_clipbybox2d": {
            "post": {
                "tags": ["(rpc) st_clipbybox2d"],
                "summary": "args: geom, box - Returns the portion of a geometry falling within a rectangle.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "box"],
                            "type": "object",
                            "description": "args: geom, box - Returns the portion of a geometry falling within a rectangle.",
                            "properties": {
                                "box": {"format": "box2d", "type": "string"},
                                "geom": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_locatebetweenelevations": {
            "post": {
                "tags": ["(rpc) st_locatebetweenelevations"],
                "summary": "args: geom_mline, elevation_start, elevation_end - Return a derived geometry (collection) value with elements that intersect the specified range of elevations inclusively. Only 3D, 4D LINESTRINGS and MULTILINESTRINGS are supported.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometry", "fromelevation", "toelevation"],
                            "type": "object",
                            "description": "args: geom_mline, elevation_start, elevation_end - Return a derived geometry (collection) value with elements that intersect the specified range of elevations inclusively. Only 3D, 4D LINESTRINGS and MULTILINESTRINGS are supported.",
                            "properties": {
                                "toelevation": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "fromelevation": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "geometry": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_hash": {
            "post": {
                "tags": ["(rpc) raster_hash"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_index": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_index"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_same": {
            "post": {
                "tags": ["(rpc) raster_same"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_collect": {
            "post": {
                "tags": ["(rpc) st_collect"],
                "summary": "args: g1, g2 - Return a specified ST_Geometry value from a collection of other geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Return a specified ST_Geometry value from a collection of other geometries.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_envelope": {
            "post": {
                "tags": ["(rpc) st_envelope"],
                "summary": "args: g1 - Returns a geometry representing the double precision (float8) bounding box of the supplied geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Returns a geometry representing the double precision (float8) bounding box of the supplied geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/updaterastersrid": {
            "post": {
                "tags": ["(rpc) updaterastersrid"],
                "summary": "args: schema_name, table_name, column_name, new_srid - Change the SRID of all rasters in the user-specified column and table.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "schema_name",
                                "table_name",
                                "column_name",
                                "new_srid",
                            ],
                            "type": "object",
                            "description": "args: schema_name, table_name, column_name, new_srid - Change the SRID of all rasters in the user-specified column and table.",
                            "properties": {
                                "new_srid": {"format": "integer", "type": "integer"},
                                "table_name": {"format": "name", "type": "string"},
                                "column_name": {"format": "name", "type": "string"},
                                "schema_name": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_le": {
            "post": {
                "tags": ["(rpc) geography_le"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_orderingequals": {
            "post": {
                "tags": ["(rpc) _st_orderingequals"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometrya", "geometryb"],
                            "type": "object",
                            "properties": {
                                "geometryb": {"format": "geometry", "type": "string"},
                                "geometrya": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_covers": {
            "post": {
                "tags": ["(rpc) st_covers"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastB lie outside raster rastA.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if no points of raster rastB lie outside raster rastA.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/checkauthtrigger": {
            "post": {
                "tags": ["(rpc) checkauthtrigger"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelascentroid": {
            "post": {
                "tags": ["(rpc) st_pixelascentroid"],
                "summary": "args: rast, x, y - Returns the centroid (point geometry) of the area represented by a pixel.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "x", "y"],
                            "type": "object",
                            "description": "args: rast, x, y - Returns the centroid (point geometry) of the area represented by a pixel.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "x": {"format": "integer", "type": "integer"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_longestline": {
            "post": {
                "tags": ["(rpc) st_longestline"],
                "summary": "args: g1, g2 - Returns the 2-dimensional longest line points of two geometries. The function will only return the first longest line if more than one, that the function finds. The line returned will always start in g1 and end in g2. The length of the line this function returns will always be the same as st_maxdistance returns for g1 and g2.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 2-dimensional longest line points of two geometries. The function will only return the first longest line if more than one, that the function finds. The line returned will always start in g1 and end in g2. The length of the line this function returns will always be the same as st_maxdistance returns for g1 and g2.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_aslatlontext": {
            "post": {
                "tags": ["(rpc) st_aslatlontext"],
                "summary": "args: pt, format=' - Return the Degrees, Minutes, Seconds representation of the given point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: pt, format=' - Return the Degrees, Minutes, Seconds representation of the given point.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "tmpl": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gidx_out": {
            "post": {
                "tags": ["(rpc) gidx_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_num_bands": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_num_bands"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box3d_out": {
            "post": {
                "tags": ["(rpc) box3d_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_spatially_unique": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_spatially_unique"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_approxquantile": {
            "post": {
                "tags": ["(rpc) st_approxquantile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastertable",
                                "rastercolumn",
                                "nband",
                                "exclude_nodata_value",
                                "sample_percent",
                                "quantile",
                            ],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "quantile": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_above": {
            "post": {
                "tags": ["(rpc) raster_above"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_perimeter2d": {
            "post": {
                "tags": ["(rpc) st_perimeter2d"],
                "summary": "args: geomA - Returns the 2-dimensional perimeter of the geometry, if it is a polygon or multi-polygon. This is currently an alias for ST_Perimeter.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns the 2-dimensional perimeter of the geometry, if it is a polygon or multi-polygon. This is currently an alias for ST_Perimeter.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_gdaldrivers": {
            "post": {
                "tags": ["(rpc) st_gdaldrivers"],
                "summary": "args: OUT idx, OUT short_name, OUT long_name, OUT create_options - Returns a list of raster formats supported by your lib gdal. These are the formats you can output your raster using ST_AsGDALRaster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: OUT idx, OUT short_name, OUT long_name, OUT create_options - Returns a list of raster formats supported by your lib gdal. These are the formats you can output your raster using ST_AsGDALRaster.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_gmltosql": {
            "post": {
                "tags": ["(rpc) st_gmltosql"],
                "summary": "args: geomgml, srid - Return a specified ST_Geometry value from GML representation. This is an alias name for ST_GeomFromGML",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomgml, srid - Return a specified ST_Geometry value from GML representation. This is an alias name for ST_GeomFromGML",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_voronoipolygons": {
            "post": {
                "tags": ["(rpc) st_voronoipolygons"],
                "summary": "args: g1, tolerance, extend_to - Returns the cells of the Voronoi diagram constructed from the vertices of a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["g1"],
                            "type": "object",
                            "description": "args: g1, tolerance, extend_to - Returns the cells of the Voronoi diagram constructed from the vertices of a geometry.",
                            "properties": {
                                "extend_to": {"format": "geometry", "type": "string"},
                                "g1": {"format": "geometry", "type": "string"},
                                "tolerance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_invdistweight4ma": {
            "post": {
                "tags": ["(rpc) st_invdistweight4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_srid": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_blocksize": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_blocksize"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastschema",
                                "rasttable",
                                "rastcolumn",
                                "axis",
                            ],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "axis": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_same": {
            "post": {
                "tags": ["(rpc) geography_gist_same"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makepointm": {
            "post": {
                "tags": ["(rpc) st_makepointm"],
                "summary": "args: x, y, m - Creates a point geometry with an x y and m coordinate.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double"],
                            "type": "object",
                            "description": "args: x, y, m - Creates a point geometry with an x y and m coordinate.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_relate": {
            "post": {
                "tags": ["(rpc) st_relate"],
                "summary": "args: geomA, geomB, intersectionMatrixPattern - Returns true if this Geometry is spatially related to anotherGeometry, by testing for intersections between the Interior, Boundary and Exterior of the two geometries as specified by the values in the intersectionMatrixPattern. If no intersectionMatrixPattern is passed in, then returns the maximum intersectionMatrixPattern that relates the 2 geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: geomA, geomB, intersectionMatrixPattern - Returns true if this Geometry is spatially related to anotherGeometry, by testing for intersections between the Interior, Boundary and Exterior of the two geometries as specified by the values in the intersectionMatrixPattern. If no intersectionMatrixPattern is passed in, then returns the maximum intersectionMatrixPattern that relates the 2 geometries.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_voronoi": {
            "post": {
                "tags": ["(rpc) _st_voronoi"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["g1"],
                            "type": "object",
                            "properties": {
                                "g1": {"format": "geometry", "type": "string"},
                                "return_polygons": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "clip": {"format": "geometry", "type": "string"},
                                "tolerance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distance": {
            "post": {
                "tags": ["(rpc) st_distance"],
                "summary": "args: g1, g2 - For geometry type Returns the 2D Cartesian distance between two geometries in projected units (based on spatial ref). For geography type defaults to return minimum geodesic distance between two geographies in meters.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - For geometry type Returns the 2D Cartesian distance between two geometries in projected units (based on spatial ref). For geography type defaults to return minimum geodesic distance between two geographies in meters.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_findextent": {
            "post": {
                "tags": ["(rpc) st_findextent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_clusterdbscan": {
            "post": {
                "tags": ["(rpc) st_clusterdbscan"],
                "summary": "args: geom, eps, minpoints - Windowing function that returns integer id for the cluster each input geometry is in based on 2D implementation of Density-based spatial clustering of applications with noise (DBSCAN) algorithm.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["eps", "minpoints"],
                            "type": "object",
                            "description": "args: geom, eps, minpoints - Windowing function that returns integer id for the cluster each input geometry is in based on 2D implementation of Density-based spatial clustering of applications with noise (DBSCAN) algorithm.",
                            "properties": {
                                "minpoints": {"format": "integer", "type": "integer"},
                                "eps": {"format": "double precision", "type": "number"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_asgml": {
            "post": {
                "tags": ["(rpc) _st_asgml"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_postgis_join_selectivity": {
            "post": {
                "tags": ["(rpc) _postgis_join_selectivity"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multipolyfromwkb": {
            "post": {
                "tags": ["(rpc) st_multipolyfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_bestsrid": {
            "post": {
                "tags": ["(rpc) _st_bestsrid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_roughness4ma": {
            "post": {
                "tags": ["(rpc) _st_roughness4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setupperleft": {
            "post": {
                "tags": ["(rpc) st_setupperleft"],
                "summary": "args: rast, x, y - Sets the value of the upper left corner of the pixel to projected X and Y coordinates.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "upperleftx", "upperlefty"],
                            "type": "object",
                            "description": "args: rast, x, y - Sets the value of the upper left corner of the pixel to projected X and Y coordinates.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "upperlefty": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "upperleftx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_skewy": {
            "post": {
                "tags": ["(rpc) st_skewy"],
                "summary": "args: rast - Returns the georeference Y skew (or rotation parameter).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the georeference Y skew (or rotation parameter).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_distance_cpa": {
            "post": {
                "tags": ["(rpc) geometry_distance_cpa"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bandnodatavalue": {
            "post": {
                "tags": ["(rpc) st_bandnodatavalue"],
                "summary": "args: rast, bandnum=1 - Returns the value in a given band that represents no data. If no band num 1 is assumed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, bandnum=1 - Returns the value in a given band that represents no data. If no band num 1 is assumed.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_srid": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_getbbox": {
            "post": {
                "tags": ["(rpc) postgis_getbbox"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_locatealong": {
            "post": {
                "tags": ["(rpc) st_locatealong"],
                "summary": "args: ageom_with_measure, a_measure, offset - Return a derived geometry collection value with elements that match the specified measure. Polygonal elements are not supported.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometry", "measure"],
                            "type": "object",
                            "description": "args: ageom_with_measure, a_measure, offset - Return a derived geometry collection value with elements that match the specified measure. Polygonal elements are not supported.",
                            "properties": {
                                "geometry": {"format": "geometry", "type": "string"},
                                "measure": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "leftrightoffset": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geographyfromtext": {
            "post": {
                "tags": ["(rpc) st_geographyfromtext"],
                "summary": "args: EWKT - Return a specified geography value from Well-Known Text representation or extended (WKT).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: EWKT - Return a specified geography value from Well-Known Text representation or extended (WKT).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_send": {
            "post": {
                "tags": ["(rpc) geography_send"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linestringfromwkb": {
            "post": {
                "tags": ["(rpc) st_linestringfromwkb"],
                "summary": "args: WKB, srid - Makes a geometry from WKB with the given SRID.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKB, srid - Makes a geometry from WKB with the given SRID.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_forcecollection": {
            "post": {
                "tags": ["(rpc) st_forcecollection"],
                "summary": "args: geomA - Convert the geometry into a GEOMETRYCOLLECTION.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Convert the geometry into a GEOMETRYCOLLECTION.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_blocksize": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_blocksize"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastschema",
                                "rasttable",
                                "rastcolumn",
                                "axis",
                            ],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "axis": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_aspng": {
            "post": {
                "tags": ["(rpc) st_aspng"],
                "summary": "args: rast, nbands, options=NULL - Return the raster tile selected bands as a single portable network graphics (PNG) image (byte array). If 1, 3, or 4 bands in raster and no bands are specified, then all bands are used. If more 2 or more than 4 bands and no bands specified, then only band 1 is used. Bands are mapped to RGB or RGBA space.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nbands"],
                            "type": "object",
                            "description": "args: rast, nbands, options=NULL - Return the raster tile selected bands as a single portable network graphics (PNG) image (byte array). If 1, 3, or 4 bands in raster and no bands are specified, then all bands are used. If more 2 or more than 4 bands and no bands specified, then only band 1 is used. Bands are mapped to RGB or RGBA space.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nbands": {"format": "integer[]", "type": "string"},
                                "options": {"format": "text[]", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_locate_along_measure": {
            "post": {
                "tags": ["(rpc) st_locate_along_measure"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_memcollect": {
            "post": {
                "tags": ["(rpc) st_memcollect"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_sum4ma": {
            "post": {
                "tags": ["(rpc) st_sum4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_liblwgeom_version": {
            "post": {
                "tags": ["(rpc) postgis_liblwgeom_version"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_tile": {
            "post": {
                "tags": ["(rpc) _st_tile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "width", "height"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "height": {"format": "integer", "type": "integer"},
                                "nband": {"format": "integer[]", "type": "string"},
                                "nodataval": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "padwithnodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_affine": {
            "post": {
                "tags": ["(rpc) st_affine"],
                "summary": "args: geomA, a, b, c, d, e, f, g, h, i, xoff, yoff, zoff - Apply a 3d affine transformation to a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                                "double",
                            ],
                            "type": "object",
                            "description": "args: geomA, a, b, c, d, e, f, g, h, i, xoff, yoff, zoff - Apply a 3d affine transformation to a geometry.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_analyze": {
            "post": {
                "tags": ["(rpc) geography_analyze"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_point": {
            "post": {
                "tags": ["(rpc) st_point"],
                "summary": "args: x_lon, y_lat - Returns an ST_Point with the given coordinate values. OGC alias for ST_MakePoint.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double"],
                            "type": "object",
                            "description": "args: x_lon, y_lat - Returns an ST_Point with the given coordinate values. OGC alias for ST_MakePoint.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_dfullywithin": {
            "post": {
                "tags": ["(rpc) _st_dfullywithin"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast1",
                                "nband1",
                                "rast2",
                                "nband2",
                                "distance",
                            ],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "distance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_iscollection": {
            "post": {
                "tags": ["(rpc) st_iscollection"],
                "summary": "args: g - Returns TRUE if the argument is a collection (MULTI*, GEOMETRYCOLLECTION, ...)",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Returns TRUE if the argument is a collection (MULTI*, GEOMETRYCOLLECTION, ...)",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_centroid": {
            "post": {
                "tags": ["(rpc) st_centroid"],
                "summary": "args: g1 - Returns the geometric center of a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Returns the geometric center of a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_snap": {
            "post": {
                "tags": ["(rpc) st_snap"],
                "summary": "args: input, reference, tolerance - Snap segments and vertices of input geometry to vertices of a reference geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2", "double"],
                            "type": "object",
                            "description": "args: input, reference, tolerance - Snap segments and vertices of input geometry to vertices of a reference geometry.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"},
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rotation": {
            "post": {
                "tags": ["(rpc) st_rotation"],
                "summary": "args: rast - Returns the rotation of the raster in radian.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the rotation of the raster in radian.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makevalid": {
            "post": {
                "tags": ["(rpc) st_makevalid"],
                "summary": "args: input - Attempts to make an invalid geometry valid without losing vertices.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: input - Attempts to make an invalid geometry valid without losing vertices.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_numbands": {
            "post": {
                "tags": ["(rpc) st_numbands"],
                "summary": "args: rast - Returns the number of bands in the raster object.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the number of bands in the raster object.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/point": {
            "post": {
                "tags": ["(rpc) point"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_num_bands": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_num_bands"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_scripts_released": {
            "post": {
                "tags": ["(rpc) postgis_scripts_released"],
                "summary": "Returns the version number of the postgis.sql script released with the installed postgis lib.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns the version number of the postgis.sql script released with the installed postgis lib.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force_2d": {
            "post": {
                "tags": ["(rpc) st_force_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_stddev4ma": {
            "post": {
                "tags": ["(rpc) st_stddev4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_num_bands": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_num_bands"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_symmetricdifference": {
            "post": {
                "tags": ["(rpc) st_symmetricdifference"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromtwkb": {
            "post": {
                "tags": ["(rpc) st_geomfromtwkb"],
                "summary": 'args: twkb - Creates a geometry instance from a TWKB ("Tiny Well-Known Binary") geometry representation.',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": 'args: twkb - Creates a geometry instance from a TWKB ("Tiny Well-Known Binary") geometry representation.',
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_contains": {
            "post": {
                "tags": ["(rpc) _st_contains"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_polygonfromwkb": {
            "post": {
                "tags": ["(rpc) st_polygonfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_minpossiblevalue": {
            "post": {
                "tags": ["(rpc) st_minpossiblevalue"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["pixeltype"],
                            "type": "object",
                            "properties": {
                                "pixeltype": {"format": "text", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asgml": {
            "post": {
                "tags": ["(rpc) st_asgml"],
                "summary": "args: version, geom, maxdecimaldigits=15, options=0, nprefix=null, id=null - Return the geometry as a GML version 2 or 3 element.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["version", "geom"],
                            "type": "object",
                            "description": "args: version, geom, maxdecimaldigits=15, options=0, nprefix=null, id=null - Return the geometry as a GML version 2 or 3 element.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "nprefix": {"format": "text", "type": "string"},
                                "version": {"format": "integer", "type": "integer"},
                                "id": {"format": "text", "type": "string"},
                                "options": {"format": "integer", "type": "integer"},
                                "maxdecimaldigits": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_le": {
            "post": {
                "tags": ["(rpc) geometry_le"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_regular_blocking": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_regular_blocking"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/addrasterconstraints": {
            "post": {
                "tags": ["(rpc) addrasterconstraints"],
                "summary": "args: rastschema, rasttable, rastcolumn, srid=true, scale_x=true, scale_y=true, blocksize_x=true, blocksize_y=true, same_alignment=true, regular_blocking=false, num_bands=true, pixel_types=true, nodata_values=true, out_db=true, extent=true - Adds raster constraints to a loaded raster table for a specific column that constrains spatial ref, scaling, blocksize, alignment, bands, band type and a flag to denote if raster column is regularly blocked. The table must be loaded with data for the constraints to be inferred. Returns true of the constraint setting was accomplished and if issues a notice.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "description": "args: rastschema, rasttable, rastcolumn, srid=true, scale_x=true, scale_y=true, blocksize_x=true, blocksize_y=true, same_alignment=true, regular_blocking=false, num_bands=true, pixel_types=true, nodata_values=true, out_db=true, extent=true - Adds raster constraints to a loaded raster table for a specific column that constrains spatial ref, scaling, blocksize, alignment, bands, band type and a flag to denote if raster column is regularly blocked. The table must be loaded with data for the constraints to be inferred. Returns true of the constraint setting was accomplished and if issues a notice.",
                            "properties": {
                                "srid": {"format": "boolean", "type": "boolean"},
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "num_bands": {"format": "boolean", "type": "boolean"},
                                "extent": {"format": "boolean", "type": "boolean"},
                                "scale_y": {"format": "boolean", "type": "boolean"},
                                "pixel_types": {"format": "boolean", "type": "boolean"},
                                "regular_blocking": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "out_db": {"format": "boolean", "type": "boolean"},
                                "scale_x": {"format": "boolean", "type": "boolean"},
                                "same_alignment": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "blocksize_y": {"format": "boolean", "type": "boolean"},
                                "blocksize_x": {"format": "boolean", "type": "boolean"},
                                "nodata_values": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makeline": {
            "post": {
                "tags": ["(rpc) st_makeline"],
                "summary": "args: geom1, geom2 - Creates a Linestring from point, multipoint, or line geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: geom1, geom2 - Creates a Linestring from point, multipoint, or line geometries.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enermaps_query_geojson": {
            "post": {
                "tags": ["(rpc) enermaps_query_geojson"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["parameters"],
                            "type": "object",
                            "properties": {
                                "row_offset": {"format": "integer", "type": "integer"},
                                "row_limit": {"format": "integer", "type": "integer"},
                                "parameters": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_dropbbox": {
            "post": {
                "tags": ["(rpc) postgis_dropbbox"],
                "summary": "args: geomA - Drop the bounding box cache from the geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Drop the bounding box cache from the geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box3dtobox": {
            "post": {
                "tags": ["(rpc) box3dtobox"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_containsproperly": {
            "post": {
                "tags": ["(rpc) st_containsproperly"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if rastB intersects the interior of rastA but not the boundary or exterior of rastA.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if rastB intersects the interior of rastA but not the boundary or exterior of rastA.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_simplifyvw": {
            "post": {
                "tags": ["(rpc) st_simplifyvw"],
                "summary": 'args: geomA, tolerance - Returns a "simplified" version of the given geometry using the Visvalingam-Whyatt algorithm',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": 'args: geomA, tolerance - Returns a "simplified" version of the given geometry using the Visvalingam-Whyatt algorithm',
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_polygon": {
            "post": {
                "tags": ["(rpc) st_polygon"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_dumppoints": {
            "post": {
                "tags": ["(rpc) _st_dumppoints"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["the_geom", "cur_path"],
                            "type": "object",
                            "properties": {
                                "cur_path": {"format": "integer[]", "type": "string"},
                                "the_geom": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isvalid": {
            "post": {
                "tags": ["(rpc) st_isvalid"],
                "summary": "args: g, flags - Returns true if the ST_Geometry is well formed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g, flags - Returns true if the ST_Geometry is well formed.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_simplifypreservetopology": {
            "post": {
                "tags": ["(rpc) st_simplifypreservetopology"],
                "summary": 'args: geomA, tolerance - Returns a "simplified" version of the given geometry using the Douglas-Peucker algorithm. Will avoid creating derived geometries (polygons in particular) that are invalid.',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": 'args: geomA, tolerance - Returns a "simplified" version of the given geometry using the Douglas-Peucker algorithm. Will avoid creating derived geometries (polygons in particular) that are invalid.',
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mpolyfromtext": {
            "post": {
                "tags": ["(rpc) st_mpolyfromtext"],
                "summary": "args: WKT, srid - Makes a MultiPolygon Geometry from WKT with the given SRID. If SRID is not give, it defaults to 0.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Makes a MultiPolygon Geometry from WKT with the given SRID. If SRID is not give, it defaults to 0.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enablelongtransactions": {
            "post": {
                "tags": ["(rpc) enablelongtransactions"],
                "summary": "Enable long transaction support. This function creates the required metadata tables, needs to be called once before using the other functions in this section. Calling it twice is harmless.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Enable long transaction support. This function creates the required metadata tables, needs to be called once before using the other functions in this section. Calling it twice is harmless.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_roughness": {
            "post": {
                "tags": ["(rpc) st_roughness"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "customextent"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "customextent": {"format": "raster", "type": "string"},
                                "interpolate_nodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/dropoverviewconstraints": {
            "post": {
                "tags": ["(rpc) dropoverviewconstraints"],
                "summary": "args: ovschema, ovtable, ovcolumn - Untag a raster column from being an overview of another.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["ovschema", "ovtable", "ovcolumn"],
                            "type": "object",
                            "description": "args: ovschema, ovtable, ovcolumn - Untag a raster column from being an overview of another.",
                            "properties": {
                                "ovcolumn": {"format": "name", "type": "string"},
                                "ovschema": {"format": "name", "type": "string"},
                                "ovtable": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bandmetadata": {
            "post": {
                "tags": ["(rpc) st_bandmetadata"],
                "summary": "args: rast, bandnum=1 - Returns basic meta data for a specific raster band. band num 1 is assumed if none-specified.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, bandnum=1 - Returns basic meta data for a specific raster band. band num 1 is assumed if none-specified.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/polygon": {
            "post": {
                "tags": ["(rpc) polygon"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_raster_lib_version": {
            "post": {
                "tags": ["(rpc) postgis_raster_lib_version"],
                "summary": "Reports full raster version and build configuration infos.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Reports full raster version and build configuration infos.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_shift_longitude": {
            "post": {
                "tags": ["(rpc) st_shift_longitude"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_right": {
            "post": {
                "tags": ["(rpc) raster_right"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_compress_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_compress_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3ddfullywithin": {
            "post": {
                "tags": ["(rpc) st_3ddfullywithin"],
                "summary": "args: g1, g2, distance - Returns true if all of the 3D geometries are within the specified distance of one another.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2", "double"],
                            "type": "object",
                            "description": "args: g1, g2, distance - Returns true if all of the 3D geometries are within the specified distance of one another.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"},
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_length": {
            "post": {
                "tags": ["(rpc) st_length"],
                "summary": "args: geog, use_spheroid=true - Returns the 2D length of the geometry if it is a LineString or MultiLineString. geometry are in units of spatial reference and geography are in meters (default spheroid)",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geog"],
                            "type": "object",
                            "description": "args: geog, use_spheroid=true - Returns the 2D length of the geometry if it is a LineString or MultiLineString. geometry are in units of spatial reference and geography are in meters (default spheroid)",
                            "properties": {
                                "geog": {"format": "geography", "type": "string"},
                                "use_spheroid": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_max4ma": {
            "post": {
                "tags": ["(rpc) st_max4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_minimumboundingradius": {
            "post": {
                "tags": ["(rpc) st_minimumboundingradius"],
                "summary": "args: geom - Returns the center point and radius of the smallest circle that can fully contain a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom - Returns the center point and radius of the smallest circle that can fully contain a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_srid": {
            "post": {
                "tags": ["(rpc) st_srid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geog"],
                            "type": "object",
                            "properties": {
                                "geog": {"format": "geography", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enermaps_get_legend": {
            "post": {
                "tags": ["(rpc) enermaps_get_legend"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["parameters"],
                            "type": "object",
                            "properties": {
                                "parameters": {"format": "text", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pointfromwkb": {
            "post": {
                "tags": ["(rpc) st_pointfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_blocksize": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_blocksize"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastschema",
                                "rasttable",
                                "rastcolumn",
                                "axis",
                            ],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "axis": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_issimple": {
            "post": {
                "tags": ["(rpc) st_issimple"],
                "summary": "args: geomA - Returns (TRUE) if this Geometry has no anomalous geometric points, such as self intersection or self tangency.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns (TRUE) if this Geometry has no anomalous geometric points, such as self intersection or self tangency.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_union_transfn": {
            "post": {
                "tags": ["(rpc) _st_union_transfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rotatex": {
            "post": {
                "tags": ["(rpc) st_rotatex"],
                "summary": "args: geomA, rotRadians - Rotate a geometry rotRadians about the X axis.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: geomA, rotRadians - Rotate a geometry rotRadians about the X axis.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_expand": {
            "post": {
                "tags": ["(rpc) _st_expand"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dextent": {
            "post": {
                "tags": ["(rpc) st_3dextent"],
                "summary": "args: geomfield - an aggregate function that returns the box3D bounding box that bounds rows of geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomfield - an aggregate function that returns the box3D bounding box that bounds rows of geometries.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/unlockrows": {
            "post": {
                "tags": ["(rpc) unlockrows"],
                "summary": "args: auth_token - Remove all locks held by specified authorization id. Returns the number of locks released.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: auth_token - Remove all locks held by specified authorization id. Returns the number of locks released.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/lockrow": {
            "post": {
                "tags": ["(rpc) lockrow"],
                "summary": "args: a_table_name, a_row_key, an_auth_token, expire_dt - Set lock/authorization for specific row in table",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["timestamp"],
                            "type": "object",
                            "description": "args: a_table_name, a_row_key, an_auth_token, expire_dt - Set lock/authorization for specific row in table",
                            "properties": {
                                "timestamp": {
                                    "format": "without time zone",
                                    "type": "string",
                                }
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/overlaps_2d": {
            "post": {
                "tags": ["(rpc) overlaps_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_colormap": {
            "post": {
                "tags": ["(rpc) st_colormap"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "colormap": {"format": "text", "type": "string"},
                                "method": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_makebox2d": {
            "post": {
                "tags": ["(rpc) st_makebox2d"],
                "summary": "args: pointLowLeft, pointUpRight - Creates a BOX2D defined by the given point geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: pointLowLeft, pointUpRight - Creates a BOX2D defined by the given point geometries.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_picksplit_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_picksplit_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_longestline": {
            "post": {
                "tags": ["(rpc) _st_longestline"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asewkb": {
            "post": {
                "tags": ["(rpc) st_asewkb"],
                "summary": "args: g1, NDR_or_XDR - Return the Well-Known Binary (WKB) representation of the geometry with SRID meta data.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1, NDR_or_XDR - Return the Well-Known Binary (WKB) representation of the geometry with SRID meta data.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_y": {
            "post": {
                "tags": ["(rpc) st_y"],
                "summary": "args: a_point - Return the Y coordinate of the point, or NULL if not available. Input must be a point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_point - Return the Y coordinate of the point, or NULL if not available. Input must be a point.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_summarystats_finalfn": {
            "post": {
                "tags": ["(rpc) _st_summarystats_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_penalty_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_penalty_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_distance_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_distance_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_updaterastersrid": {
            "post": {
                "tags": ["(rpc) _updaterastersrid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "schema_name",
                                "table_name",
                                "column_name",
                                "new_srid",
                            ],
                            "type": "object",
                            "properties": {
                                "new_srid": {"format": "integer", "type": "integer"},
                                "table_name": {"format": "name", "type": "string"},
                                "column_name": {"format": "name", "type": "string"},
                                "schema_name": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_concavehull": {
            "post": {
                "tags": ["(rpc) _st_concavehull"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["param_inputgeom"],
                            "type": "object",
                            "properties": {
                                "param_inputgeom": {
                                    "format": "geometry",
                                    "type": "string",
                                }
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_raster_contain": {
            "post": {
                "tags": ["(rpc) geometry_raster_contain"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dlongestline": {
            "post": {
                "tags": ["(rpc) st_3dlongestline"],
                "summary": "args: g1, g2 - Returns the 3-dimensional longest line between two geometries",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 3-dimensional longest line between two geometries",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geometryfromtext": {
            "post": {
                "tags": ["(rpc) st_geometryfromtext"],
                "summary": "args: WKT, srid - Return a specified ST_Geometry value from Well-Known Text representation (WKT). This is an alias name for ST_GeomFromText",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Return a specified ST_Geometry value from Well-Known Text representation (WKT). This is an alias name for ST_GeomFromText",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_reclass": {
            "post": {
                "tags": ["(rpc) st_reclass"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "reclassexpr", "pixeltype"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "nodataval": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "pixeltype": {"format": "text", "type": "string"},
                                "reclassexpr": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_area2d": {
            "post": {
                "tags": ["(rpc) st_area2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_numpoints": {
            "post": {
                "tags": ["(rpc) st_numpoints"],
                "summary": "args: g1 - Return the number of points in an ST_LineString or ST_CircularString value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the number of points in an ST_LineString or ST_CircularString value.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_libxml_version": {
            "post": {
                "tags": ["(rpc) postgis_libxml_version"],
                "summary": "Returns the version number of the libxml2 library.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns the version number of the libxml2 library.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_buildarea": {
            "post": {
                "tags": ["(rpc) st_buildarea"],
                "summary": "args: A - Creates an areal geometry formed by the constituent linework of given geometry",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: A - Creates an areal geometry formed by the constituent linework of given geometry",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_collectionhomogenize": {
            "post": {
                "tags": ["(rpc) st_collectionhomogenize"],
                "summary": 'args: collection - Given a geometry collection, return the "simplest" representation of the contents.',
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": 'args: collection - Given a geometry collection, return the "simplest" representation of the contents.',
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_npoints": {
            "post": {
                "tags": ["(rpc) st_npoints"],
                "summary": "args: g1 - Return the number of points (vertexes) in a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the number of points (vertexes) in a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_upperleftx": {
            "post": {
                "tags": ["(rpc) st_upperleftx"],
                "summary": "args: rast - Returns the upper left X coordinate of raster in projected spatial ref.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the upper left X coordinate of raster in projected spatial ref.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geotransform": {
            "post": {
                "tags": ["(rpc) st_geotransform"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_analyze": {
            "post": {
                "tags": ["(rpc) geometry_analyze"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_resample": {
            "post": {
                "tags": ["(rpc) st_resample"],
                "summary": "args: rast, width, height, gridx=NULL, gridy=NULL, skewx=0, skewy=0, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster using a specified resampling algorithm, new dimensions, an arbitrary grid corner and a set of raster georeferencing attributes defined or borrowed from another raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "width", "height"],
                            "type": "object",
                            "description": "args: rast, width, height, gridx=NULL, gridy=NULL, skewx=0, skewy=0, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster using a specified resampling algorithm, new dimensions, an arbitrary grid corner and a set of raster georeferencing attributes defined or borrowed from another raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "height": {"format": "integer", "type": "integer"},
                                "gridx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "width": {"format": "integer", "type": "integer"},
                                "gridy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "algorithm": {"format": "text", "type": "string"},
                                "skewx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "skewy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_combine_bbox": {
            "post": {
                "tags": ["(rpc) st_combine_bbox"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint_nodata_values": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint_nodata_values"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_union_2d": {
            "post": {
                "tags": ["(rpc) geometry_gist_union_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_nearestvalue": {
            "post": {
                "tags": ["(rpc) st_nearestvalue"],
                "summary": "args: rast, bandnum, columnx, rowy, exclude_nodata_value=true - Returns the nearest non-NODATA value of a given bands pixel specified by a columnx and rowy or a geometric point expressed in the same spatial reference coordinate system as the raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "band", "columnx", "rowy"],
                            "type": "object",
                            "description": "args: rast, bandnum, columnx, rowy, exclude_nodata_value=true - Returns the nearest non-NODATA value of a given bands pixel specified by a columnx and rowy or a geometric point expressed in the same spatial reference coordinate system as the raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "rowy": {"format": "integer", "type": "integer"},
                                "columnx": {"format": "integer", "type": "integer"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/populate_geometry_columns": {
            "post": {
                "tags": ["(rpc) populate_geometry_columns"],
                "summary": "args: relation_oid, use_typmod=true - Ensures geometry columns are defined with type modifiers or have appropriate spatial constraints This ensures they will be registered correctly in geometry_columns view. By default will convert all geometry columns with no type modifier to ones with type modifiers. To get old behavior set use_typmod=false",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["tbl_oid"],
                            "type": "object",
                            "description": "args: relation_oid, use_typmod=true - Ensures geometry columns are defined with type modifiers or have appropriate spatial constraints This ensures they will be registered correctly in geometry_columns view. By default will convert all geometry columns with no type modifier to ones with type modifiers. To get old behavior set use_typmod=false",
                            "properties": {
                                "tbl_oid": {"format": "oid", "type": "string"},
                                "use_typmod": {"format": "boolean", "type": "boolean"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_accum": {
            "post": {
                "tags": ["(rpc) st_accum"],
                "summary": "args: geomfield - Aggregate. Constructs an array of geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomfield - Aggregate. Constructs an array of geometries.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/disablelongtransactions": {
            "post": {
                "tags": ["(rpc) disablelongtransactions"],
                "summary": "Disable long transaction support. This function removes the long transaction support metadata tables, and drops all triggers attached to lock-checked tables.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Disable long transaction support. This function removes the long transaction support metadata tables, and drops all triggers attached to lock-checked tables.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint_nodata_values": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint_nodata_values"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_send": {
            "post": {
                "tags": ["(rpc) geometry_send"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_addmeasure": {
            "post": {
                "tags": ["(rpc) st_addmeasure"],
                "summary": "args: geom_mline, measure_start, measure_end - Return a derived geometry with measure elements linearly interpolated between the start and end points.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double"],
                            "type": "object",
                            "description": "args: geom_mline, measure_start, measure_end - Return a derived geometry with measure elements linearly interpolated between the start and end points.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setvalue": {
            "post": {
                "tags": ["(rpc) st_setvalue"],
                "summary": "args: rast, bandnum, columnx, rowy, newvalue - Returns modified raster resulting from setting the value of a given band in a given columnx, rowy pixel or the pixels that intersect a particular geometry. Band numbers start at 1 and assumed to be 1 if not specified.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "band", "x", "y", "newvalue"],
                            "type": "object",
                            "description": "args: rast, bandnum, columnx, rowy, newvalue - Returns modified raster resulting from setting the value of a given band in a given columnx, rowy pixel or the pixels that intersect a particular geometry. Band numbers start at 1 and assumed to be 1 if not specified.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "newvalue": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "x": {"format": "integer", "type": "integer"},
                                "band": {"format": "integer", "type": "integer"},
                                "y": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_consistent": {
            "post": {
                "tags": ["(rpc) geography_gist_consistent"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_in": {
            "post": {
                "tags": ["(rpc) geometry_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distinct4ma": {
            "post": {
                "tags": ["(rpc) st_distinct4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_skewx": {
            "post": {
                "tags": ["(rpc) st_skewx"],
                "summary": "args: rast - Returns the georeference X skew (or rotation parameter).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the georeference X skew (or rotation parameter).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linelocatepoint": {
            "post": {
                "tags": ["(rpc) st_linelocatepoint"],
                "summary": "args: a_linestring, a_point - Returns a float between 0 and 1 representing the location of the closest point on LineString to the given Point, as a fraction of total 2d line length.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: a_linestring, a_point - Returns a float between 0 and 1 representing the location of the closest point on LineString to the given Point, as a fraction of total 2d line length.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pointn": {
            "post": {
                "tags": ["(rpc) st_pointn"],
                "summary": "args: a_linestring, n - Return the Nth point in the first LineString or circular LineString in the geometry. Negative values are counted backwards from the end of the LineString. Returns NULL if there is no linestring in the geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_linestring, n - Return the Nth point in the first LineString or circular LineString in the geometry. Negative values are counted backwards from the end of the LineString. Returns NULL if there is no linestring in the geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_picksplit": {
            "post": {
                "tags": ["(rpc) geography_gist_picksplit"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_linecrossingdirection": {
            "post": {
                "tags": ["(rpc) _st_linecrossingdirection"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_countagg": {
            "post": {
                "tags": ["(rpc) st_countagg"],
                "summary": "args: rast, nband, exclude_nodata_value, sample_percent - Aggregate. Returns the number of pixels in a given band of a set of rasters. If no band is specified defaults to band 1. If exclude_nodata_value is set to true, will only count pixels that are not equal to the NODATA value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: rast, nband, exclude_nodata_value, sample_percent - Aggregate. Returns the number of pixels in a given band of a set of rasters. If no band is specified defaults to band 1. If exclude_nodata_value is set to true, will only count pixels that are not equal to the NODATA value.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_distancetree": {
            "post": {
                "tags": ["(rpc) _st_distancetree"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_delaunaytriangles": {
            "post": {
                "tags": ["(rpc) st_delaunaytriangles"],
                "summary": "args: g1, tolerance, flags - Return a Delaunay triangulation around the given input points.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["g1"],
                            "type": "object",
                            "description": "args: g1, tolerance, flags - Return a Delaunay triangulation around the given input points.",
                            "properties": {
                                "flags": {"format": "integer", "type": "integer"},
                                "g1": {"format": "geometry", "type": "string"},
                                "tolerance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_distance": {
            "post": {
                "tags": ["(rpc) geography_gist_distance"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distancesphere": {
            "post": {
                "tags": ["(rpc) st_distancesphere"],
                "summary": "args: geomlonlatA, geomlonlatB - Returns minimum distance in meters between two lon/lat geometries. Uses a spherical earth and radius derived from the spheroid defined by the SRID. Faster than ST_DistanceSpheroid , but less accurate. PostGIS versions prior to 1.5 only implemented for points.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: geomlonlatA, geomlonlatB - Returns minimum distance in meters between two lon/lat geometries. Uses a spherical earth and radius derived from the spheroid defined by the SRID. Faster than ST_DistanceSpheroid , but less accurate. PostGIS versions prior to 1.5 only implemented for points.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_penalty": {
            "post": {
                "tags": ["(rpc) geography_gist_penalty"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_asjpeg": {
            "post": {
                "tags": ["(rpc) st_asjpeg"],
                "summary": "args: rast, nbands, quality - Return the raster tile selected bands as a single Joint Photographic Exports Group (JPEG) image (byte array). If no band is specified and 1 or more than 3 bands, then only the first band is used. If only 3 bands then all 3 bands are used and mapped to RGB.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nbands", "quality"],
                            "type": "object",
                            "description": "args: rast, nbands, quality - Return the raster tile selected bands as a single Joint Photographic Exports Group (JPEG) image (byte array). If no band is specified and 1 or more than 3 bands, then only the first band is used. If only 3 bands then all 3 bands are used and mapped to RGB.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nbands": {"format": "integer[]", "type": "string"},
                                "quality": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_within": {
            "post": {
                "tags": ["(rpc) _st_within"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_pixelaspolygons": {
            "post": {
                "tags": ["(rpc) _st_pixelaspolygons"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "rowy": {"format": "integer", "type": "integer"},
                                "columnx": {"format": "integer", "type": "integer"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_above": {
            "post": {
                "tags": ["(rpc) geometry_above"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_transscale": {
            "post": {
                "tags": ["(rpc) st_transscale"],
                "summary": "args: geomA, deltaX, deltaY, XFactor, YFactor - Translate a geometry by given factors and offsets.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double", "double"],
                            "type": "object",
                            "description": "args: geomA, deltaX, deltaY, XFactor, YFactor - Translate a geometry by given factors and offsets.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dperimeter": {
            "post": {
                "tags": ["(rpc) st_3dperimeter"],
                "summary": "args: geomA - Returns the 3-dimensional perimeter of the geometry, if it is a polygon or multi-polygon.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns the 3-dimensional perimeter of the geometry, if it is a polygon or multi-polygon.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_raster_overlap": {
            "post": {
                "tags": ["(rpc) geometry_raster_overlap"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_resize": {
            "post": {
                "tags": ["(rpc) st_resize"],
                "summary": "args: rast, width, height, algorithm=NearestNeighbor, maxerr=0.125 - Resize a raster to a new width/height",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "width", "height"],
                            "type": "object",
                            "description": "args: rast, width, height, algorithm=NearestNeighbor, maxerr=0.125 - Resize a raster to a new width/height",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "height": {"format": "text", "type": "string"},
                                "width": {"format": "text", "type": "string"},
                                "algorithm": {"format": "text", "type": "string"},
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bandisnodata": {
            "post": {
                "tags": ["(rpc) st_bandisnodata"],
                "summary": "args: rast, band, forceChecking=true - Returns true if the band is filled with only nodata values.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "description": "args: rast, band, forceChecking=true - Returns true if the band is filled with only nodata values.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "forcechecking": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_linetocurve": {
            "post": {
                "tags": ["(rpc) st_linetocurve"],
                "summary": "args: geomANoncircular - Converts a LINESTRING/POLYGON to a CIRCULARSTRING, CURVEPOLYGON",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geometry"],
                            "type": "object",
                            "description": "args: geomANoncircular - Converts a LINESTRING/POLYGON to a CIRCULARSTRING, CURVEPOLYGON",
                            "properties": {
                                "geometry": {"format": "geometry", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pixelofvalue": {
            "post": {
                "tags": ["(rpc) st_pixelofvalue"],
                "summary": "args: rast, nband, search, exclude_nodata_value=true - Get the columnx, rowy coordinates of the pixel whose value equals the search value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "search"],
                            "type": "object",
                            "description": "args: rast, nband, search, exclude_nodata_value=true - Get the columnx, rowy coordinates of the pixel whose value equals the search value.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "search": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force_4d": {
            "post": {
                "tags": ["(rpc) st_force_4d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_polyfromwkb": {
            "post": {
                "tags": ["(rpc) st_polyfromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bdmpolyfromtext": {
            "post": {
                "tags": ["(rpc) st_bdmpolyfromtext"],
                "summary": "args: WKT, srid - Construct a MultiPolygon given an arbitrary collection of closed linestrings as a MultiLineString text representation Well-Known text representation.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Construct a MultiPolygon given an arbitrary collection of closed linestrings as a MultiLineString text representation Well-Known text representation.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geometrytype": {
            "post": {
                "tags": ["(rpc) st_geometrytype"],
                "summary": "args: g1 - Return the geometry type of the ST_Geometry value.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the geometry type of the ST_Geometry value.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_abs_in": {
            "post": {
                "tags": ["(rpc) pgis_abs_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_numgeometries": {
            "post": {
                "tags": ["(rpc) st_numgeometries"],
                "summary": "args: geom - If geometry is a GEOMETRYCOLLECTION (or MULTI*) return the number of geometries, for single geometries will return 1, otherwise return NULL.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom - If geometry is a GEOMETRYCOLLECTION (or MULTI*) return the number of geometries, for single geometries will return 1, otherwise return NULL.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_length2d": {
            "post": {
                "tags": ["(rpc) st_length2d"],
                "summary": "args: a_2dlinestring - Returns the 2-dimensional length of the geometry if it is a linestring or multi-linestring. This is an alias for ST_Length",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_2dlinestring - Returns the 2-dimensional length of the geometry if it is a linestring or multi-linestring. This is an alias for ST_Length",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_forcecurve": {
            "post": {
                "tags": ["(rpc) st_forcecurve"],
                "summary": "args: g - Upcast a geometry into its curved type, if applicable.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Upcast a geometry into its curved type, if applicable.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/contains_2d": {
            "post": {
                "tags": ["(rpc) contains_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/box3d": {
            "post": {
                "tags": ["(rpc) box3d"],
                "summary": "args: geomA - Returns a BOX3D representing the maximum extents of the geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns a BOX3D representing the maximum extents of the geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geogfromwkb": {
            "post": {
                "tags": ["(rpc) st_geogfromwkb"],
                "summary": "args: wkb - Creates a geography instance from a Well-Known Binary geometry representation (WKB) or extended Well Known Binary (EWKB).",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: wkb - Creates a geography instance from a Well-Known Binary geometry representation (WKB) or extended Well Known Binary (EWKB).",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometrytype": {
            "post": {
                "tags": ["(rpc) geometrytype"],
                "summary": "args: geomA - Returns the type of the geometry as a string. Eg: LINESTRING, POLYGON, MULTIPOINT, etc.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns the type of the geometry as a string. Eg: LINESTRING, POLYGON, MULTIPOINT, etc.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_hillshade": {
            "post": {
                "tags": ["(rpc) st_hillshade"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "customextent"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "scale": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "pixeltype": {"format": "text", "type": "string"},
                                "azimuth": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "customextent": {"format": "raster", "type": "string"},
                                "altitude": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "interpolate_nodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "max_bright": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_flipcoordinates": {
            "post": {
                "tags": ["(rpc) st_flipcoordinates"],
                "summary": "args: geom - Returns a version of the given geometry with X and Y axis flipped. Useful for people who have built latitude/longitude features and need to fix them.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom - Returns a version of the given geometry with X and Y axis flipped. Useful for people who have built latitude/longitude features and need to fix them.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_union": {
            "post": {
                "tags": ["(rpc) geography_gist_union"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_tpi4ma": {
            "post": {
                "tags": ["(rpc) _st_tpi4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force3d": {
            "post": {
                "tags": ["(rpc) st_force3d"],
                "summary": "args: geomA - Force the geometries into XYZ mode. This is an alias for ST_Force3DZ.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Force the geometries into XYZ mode. This is an alias for ST_Force3DZ.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_distance_spheroid": {
            "post": {
                "tags": ["(rpc) st_distance_spheroid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_xmin": {
            "post": {
                "tags": ["(rpc) st_xmin"],
                "summary": "args: aGeomorBox2DorBox3D - Returns X minima of a bounding box 2d or 3d or a geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: aGeomorBox2DorBox3D - Returns X minima of a bounding box 2d or 3d or a geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pointinsidecircle": {
            "post": {
                "tags": ["(rpc) st_pointinsidecircle"],
                "summary": "args: a_point, center_x, center_y, radius - Is the point geometry insert circle defined by center_x, center_y, radius",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double", "double", "double"],
                            "type": "object",
                            "description": "args: a_point, center_x, center_y, radius - Is the point geometry insert circle defined by center_x, center_y, radius",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_setscale": {
            "post": {
                "tags": ["(rpc) st_setscale"],
                "summary": "args: rast, x, y - Sets the X and Y size of pixels in units of coordinate reference system. Number units/pixel width/height.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "scalex", "scaley"],
                            "type": "object",
                            "description": "args: rast, x, y - Sets the X and Y size of pixels in units of coordinate reference system. Number units/pixel width/height.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_polygonfromtext": {
            "post": {
                "tags": ["(rpc) st_polygonfromtext"],
                "summary": "args: WKT, srid - Makes a Geometry from WKT with the given SRID. If SRID is not give, it defaults to 0.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Makes a Geometry from WKT with the given SRID. If SRID is not give, it defaults to 0.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_snaptogrid": {
            "post": {
                "tags": ["(rpc) st_snaptogrid"],
                "summary": "args: rast, gridx, gridy, scalex, scaley, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster by snapping it to a grid. New pixel values are computed using the NearestNeighbor (english or american spelling), Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "gridx", "gridy", "scalex", "scaley"],
                            "type": "object",
                            "description": "args: rast, gridx, gridy, scalex, scaley, algorithm=NearestNeighbour, maxerr=0.125 - Resample a raster by snapping it to a grid. New pixel values are computed using the NearestNeighbor (english or american spelling), Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "gridx": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "gridy": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "algorithm": {"format": "text", "type": "string"},
                                "scalex": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "maxerr": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "scaley": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_alignment": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_alignment"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "rastcolumn"],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_lib_build_date": {
            "post": {
                "tags": ["(rpc) postgis_lib_build_date"],
                "summary": "Returns build date of the PostGIS library.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns build date of the PostGIS library.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/is_json_object": {
            "post": {
                "tags": ["(rpc) is_json_object"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["p_json"],
                            "type": "object",
                            "properties": {
                                "p_json": {"format": "text", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force3dm": {
            "post": {
                "tags": ["(rpc) st_force3dm"],
                "summary": "args: geomA - Force the geometries into XYM mode.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Force the geometries into XYM mode.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_cpawithin": {
            "post": {
                "tags": ["(rpc) st_cpawithin"],
                "summary": "args: track1, track2, maxdist - Returns true if the trajectories closest points of approachare within the specified distance.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: track1, track2, maxdist - Returns true if the trajectories closest points of approachare within the specified distance.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_overview_constraint_info": {
            "post": {
                "tags": ["(rpc) _overview_constraint_info"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["ovschema", "ovtable", "ovcolumn"],
                            "type": "object",
                            "properties": {
                                "ovcolumn": {"format": "name", "type": "string"},
                                "ovschema": {"format": "name", "type": "string"},
                                "ovtable": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_createoverview": {
            "post": {
                "tags": ["(rpc) st_createoverview"],
                "summary": "args: tab, col, factor, algo='NearestNeighbor' - Create an reduced resolution version of a given raster coverage.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["tab", "col", "factor"],
                            "type": "object",
                            "description": "args: tab, col, factor, algo='NearestNeighbor' - Create an reduced resolution version of a given raster coverage.",
                            "properties": {
                                "factor": {"format": "integer", "type": "integer"},
                                "tab": {"format": "regclass", "type": "string"},
                                "algo": {"format": "text", "type": "string"},
                                "col": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/enermaps_query_table": {
            "post": {
                "tags": ["(rpc) enermaps_query_table"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["parameters"],
                            "type": "object",
                            "properties": {
                                "row_offset": {"format": "integer", "type": "integer"},
                                "row_limit": {"format": "integer", "type": "integer"},
                                "parameters": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_maxdistance": {
            "post": {
                "tags": ["(rpc) st_maxdistance"],
                "summary": "args: g1, g2 - Returns the 2-dimensional largest distance between two geometries in projected units.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns the 2-dimensional largest distance between two geometries in projected units.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_multilinefromwkb": {
            "post": {
                "tags": ["(rpc) st_multilinefromwkb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/equals": {
            "post": {
                "tags": ["(rpc) equals"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gserialized_gist_sel_2d": {
            "post": {
                "tags": ["(rpc) gserialized_gist_sel_2d"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_recv": {
            "post": {
                "tags": ["(rpc) geometry_recv"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_same": {
            "post": {
                "tags": ["(rpc) geometry_same"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/spheroid_out": {
            "post": {
                "tags": ["(rpc) spheroid_out"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_gist_compress": {
            "post": {
                "tags": ["(rpc) geography_gist_compress"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_overlap": {
            "post": {
                "tags": ["(rpc) raster_overlap"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rastertoworldcoord": {
            "post": {
                "tags": ["(rpc) st_rastertoworldcoord"],
                "summary": "args: rast, xcolumn, yrow - Returns the rasters upper left corner as geometric X and Y (longitude and latitude) given a column and row. Column and row starts at 1.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "columnx", "rowy"],
                            "type": "object",
                            "description": "args: rast, xcolumn, yrow - Returns the rasters upper left corner as geometric X and Y (longitude and latitude) given a column and row. Column and row starts at 1.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "rowy": {"format": "integer", "type": "integer"},
                                "columnx": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pointfromtext": {
            "post": {
                "tags": ["(rpc) st_pointfromtext"],
                "summary": "args: WKT, srid - Makes a point Geometry from WKT with the given SRID. If SRID is not given, it defaults to unknown.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Makes a point Geometry from WKT with the given SRID. If SRID is not given, it defaults to unknown.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_equals": {
            "post": {
                "tags": ["(rpc) st_equals"],
                "summary": "args: A, B - Returns true if the given geometries represent the same geometry. Directionality is ignored.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: A, B - Returns true if the given geometries represent the same geometry. Directionality is ignored.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_removerepeatedpoints": {
            "post": {
                "tags": ["(rpc) st_removerepeatedpoints"],
                "summary": "args: geom, tolerance - Returns a version of the given geometry with duplicated points removed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom, tolerance - Returns a version of the given geometry with duplicated points removed.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "tolerance": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_overlaps": {
            "post": {
                "tags": ["(rpc) _st_overlaps"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/gettransactionid": {
            "post": {
                "tags": ["(rpc) gettransactionid"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_aspect4ma": {
            "post": {
                "tags": ["(rpc) _st_aspect4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_bdpolyfromtext": {
            "post": {
                "tags": ["(rpc) st_bdpolyfromtext"],
                "summary": "args: WKT, srid - Construct a Polygon given an arbitrary collection of closed linestrings as a MultiLineString Well-Known text representation.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: WKT, srid - Construct a Polygon given an arbitrary collection of closed linestrings as a MultiLineString Well-Known text representation.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_worldtorastercoord": {
            "post": {
                "tags": ["(rpc) st_worldtorastercoord"],
                "summary": "args: rast, longitude, latitude - Returns the upper left corner as column and row given geometric X and Y (longitude and latitude) or a point geometry expressed in the spatial reference coordinate system of the raster.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "longitude", "latitude"],
                            "type": "object",
                            "description": "args: rast, longitude, latitude - Returns the upper left corner as column and row given geometric X and Y (longitude and latitude) or a point geometry expressed in the spatial reference coordinate system of the raster.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "latitude": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "longitude": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_overlaps": {
            "post": {
                "tags": ["(rpc) geography_overlaps"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_force_3dz": {
            "post": {
                "tags": ["(rpc) st_force_3dz"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_geomfromgml": {
            "post": {
                "tags": ["(rpc) _st_geomfromgml"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_ge": {
            "post": {
                "tags": ["(rpc) geometry_ge"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_difference": {
            "post": {
                "tags": ["(rpc) st_difference"],
                "summary": "args: geomA, geomB - Returns a geometry that represents that part of geometry A that does not intersect with geometry B.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: geomA, geomB - Returns a geometry that represents that part of geometry A that does not intersect with geometry B.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_quantile": {
            "post": {
                "tags": ["(rpc) st_quantile"],
                "summary": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true, quantiles=NULL - Compute quantiles for a raster or raster table coverage in the context of the sample or population. Thus, a value could be examined to be at the rasters 25%, 50%, 75% percentile.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "description": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true, quantiles=NULL - Compute quantiles for a raster or raster table coverage in the context of the sample or population. Thus, a value could be examined to be at the rasters 25%, 50%, 75% percentile.",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "quantiles": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_numinteriorrings": {
            "post": {
                "tags": ["(rpc) st_numinteriorrings"],
                "summary": "args: a_polygon - Return the number of interior rings of a polygon geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_polygon - Return the number of interior rings of a polygon geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_nrings": {
            "post": {
                "tags": ["(rpc) st_nrings"],
                "summary": "args: geomA - If the geometry is a polygon or multi-polygon returns the number of rings.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - If the geometry is a polygon or multi-polygon returns the number of rings.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_samealignment_transfn": {
            "post": {
                "tags": ["(rpc) _st_samealignment_transfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["agg", "rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "agg": {
                                    "format": "agg_samealignment",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/pgis_geometry_makeline_finalfn": {
            "post": {
                "tags": ["(rpc) pgis_geometry_makeline_finalfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_assvg": {
            "post": {
                "tags": ["(rpc) st_assvg"],
                "summary": "args: geom, rel=0, maxdecimaldigits=15 - Returns a Geometry in SVG path data given a geometry or geography object.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom"],
                            "type": "object",
                            "description": "args: geom, rel=0, maxdecimaldigits=15 - Returns a Geometry in SVG path data given a geometry or geography object.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "rel": {"format": "integer", "type": "integer"},
                                "maxdecimaldigits": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_coveredby": {
            "post": {
                "tags": ["(rpc) _st_coveredby"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_distance_centroid_nd": {
            "post": {
                "tags": ["(rpc) geometry_distance_centroid_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_rastertoworldcoord": {
            "post": {
                "tags": ["(rpc) _st_rastertoworldcoord"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "rowy": {"format": "integer", "type": "integer"},
                                "columnx": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_pointonsurface": {
            "post": {
                "tags": ["(rpc) st_pointonsurface"],
                "summary": "args: g1 - Returns a POINT guaranteed to lie on the surface.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Returns a POINT guaranteed to lie on the surface.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_libjson_version": {
            "post": {
                "tags": ["(rpc) postgis_libjson_version"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_askml": {
            "post": {
                "tags": ["(rpc) st_askml"],
                "summary": "args: version, geom, maxdecimaldigits=15, nprefix=NULL - Return the geometry as a KML element. Several variants. Default version=2, default precision=15",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["version", "geom"],
                            "type": "object",
                            "description": "args: version, geom, maxdecimaldigits=15, nprefix=NULL - Return the geometry as a KML element. Several variants. Default version=2, default precision=15",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "nprefix": {"format": "text", "type": "string"},
                                "version": {"format": "integer", "type": "integer"},
                                "maxdecimaldigits": {
                                    "format": "integer",
                                    "type": "integer",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_geomfromwkb": {
            "post": {
                "tags": ["(rpc) st_geomfromwkb"],
                "summary": "args: geom, srid - Makes a geometry from WKB with the given SRID",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geom, srid - Makes a geometry from WKB with the given SRID",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_upperlefty": {
            "post": {
                "tags": ["(rpc) st_upperlefty"],
                "summary": "args: rast - Returns the upper left Y coordinate of raster in projected spatial ref.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: rast - Returns the upper left Y coordinate of raster in projected spatial ref.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_drop_raster_constraint": {
            "post": {
                "tags": ["(rpc) _drop_raster_constraint"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastschema", "rasttable", "cn"],
                            "type": "object",
                            "properties": {
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "cn": {"format": "name", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_equals": {
            "post": {
                "tags": ["(rpc) _st_equals"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_worldtorastercoord": {
            "post": {
                "tags": ["(rpc) _st_worldtorastercoord"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "latitude": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "longitude": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_aspect": {
            "post": {
                "tags": ["(rpc) st_aspect"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "nband", "customextent"],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "units": {"format": "text", "type": "string"},
                                "customextent": {"format": "raster", "type": "string"},
                                "interpolate_nodata": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_node": {
            "post": {
                "tags": ["(rpc) st_node"],
                "summary": "args: geom - Node a set of linestrings.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["g"],
                            "type": "object",
                            "description": "args: geom - Node a set of linestrings.",
                            "properties": {
                                "g": {"format": "geometry", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_3dmakebox": {
            "post": {
                "tags": ["(rpc) st_3dmakebox"],
                "summary": "args: point3DLowLeftBottom, point3DUpRightTop - Creates a BOX3D defined by the given 3d point geometries.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: point3DLowLeftBottom, point3DUpRightTop - Creates a BOX3D defined by the given 3d point geometries.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/raster_eq": {
            "post": {
                "tags": ["(rpc) raster_eq"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_within": {
            "post": {
                "tags": ["(rpc) geometry_within"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_raster_constraint_info_scale": {
            "post": {
                "tags": ["(rpc) _raster_constraint_info_scale"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rastschema",
                                "rasttable",
                                "rastcolumn",
                                "axis",
                            ],
                            "type": "object",
                            "properties": {
                                "rastcolumn": {"format": "name", "type": "string"},
                                "rasttable": {"format": "name", "type": "string"},
                                "rastschema": {"format": "name", "type": "string"},
                                "axis": {"format": "character", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_overleft": {
            "post": {
                "tags": ["(rpc) geometry_overleft"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_countagg_transfn": {
            "post": {
                "tags": ["(rpc) _st_countagg_transfn"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "agg",
                                "rast",
                                "nband",
                                "exclude_nodata_value",
                                "sample_percent",
                            ],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "agg": {"format": "agg_count", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_postgis_deprecate": {
            "post": {
                "tags": ["(rpc) _postgis_deprecate"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["oldname", "newname", "version"],
                            "type": "object",
                            "properties": {
                                "newname": {"format": "text", "type": "string"},
                                "version": {"format": "text", "type": "string"},
                                "oldname": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mapalgebrafctngb": {
            "post": {
                "tags": ["(rpc) st_mapalgebrafctngb"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": [
                                "rast",
                                "band",
                                "pixeltype",
                                "ngbwidth",
                                "ngbheight",
                                "onerastngbuserfunc",
                                "nodatamode",
                                "VARIADIC",
                            ],
                            "type": "object",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nodatamode": {"format": "text", "type": "string"},
                                "pixeltype": {"format": "text", "type": "string"},
                                "ngbheight": {"format": "integer", "type": "integer"},
                                "onerastngbuserfunc": {
                                    "format": "regprocedure",
                                    "type": "string",
                                },
                                "ngbwidth": {"format": "integer", "type": "integer"},
                                "VARIADIC": {"format": "args text[]", "type": "string"},
                                "band": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_swapordinates": {
            "post": {
                "tags": ["(rpc) st_swapordinates"],
                "summary": "args: geom, ords - Returns a version of the given geometry with given ordinate values swapped.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom", "ords"],
                            "type": "object",
                            "description": "args: geom, ords - Returns a version of the given geometry with given ordinate values swapped.",
                            "properties": {
                                "geom": {"format": "geometry", "type": "string"},
                                "ords": {"format": "cstring", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_histogram": {
            "post": {
                "tags": ["(rpc) st_histogram"],
                "summary": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true, bins=autocomputed, width=NULL, right=false - Returns a set of record summarizing a raster or raster coverage data distribution separate bin ranges. Number of bins are autocomputed if not specified.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "description": "args: rastertable, rastercolumn, nband=1, exclude_nodata_value=true, bins=autocomputed, width=NULL, right=false - Returns a set of record summarizing a raster or raster coverage data distribution separate bin ranges. Number of bins are autocomputed if not specified.",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "rastertable": {"format": "text", "type": "string"},
                                "width": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                                "right": {"format": "boolean", "type": "boolean"},
                                "bins": {"format": "integer", "type": "integer"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_patchn": {
            "post": {
                "tags": ["(rpc) st_patchn"],
                "summary": "args: geomA, n - Return the 1-based Nth geometry (face) if the geometry is a POLYHEDRALSURFACE, POLYHEDRALSURFACEM. Otherwise, return NULL.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA, n - Return the 1-based Nth geometry (face) if the geometry is a POLYHEDRALSURFACE, POLYHEDRALSURFACEM. Otherwise, return NULL.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_constraint_type": {
            "post": {
                "tags": ["(rpc) postgis_constraint_type"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geomschema", "geomtable", "geomcolumn"],
                            "type": "object",
                            "properties": {
                                "geomschema": {"format": "text", "type": "string"},
                                "geomcolumn": {"format": "text", "type": "string"},
                                "geomtable": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_overlaps": {
            "post": {
                "tags": ["(rpc) st_overlaps"],
                "summary": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA and rastB intersect but one does not completely contain the other.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast1", "nband1", "rast2", "nband2"],
                            "type": "object",
                            "description": "args: rastA, nbandA, rastB, nbandB - Return true if raster rastA and rastB intersect but one does not completely contain the other.",
                            "properties": {
                                "rast1": {"format": "raster", "type": "string"},
                                "nband2": {"format": "integer", "type": "integer"},
                                "nband1": {"format": "integer", "type": "integer"},
                                "rast2": {"format": "raster", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_rotatey": {
            "post": {
                "tags": ["(rpc) st_rotatey"],
                "summary": "args: geomA, rotRadians - Rotate a geometry rotRadians about the Y axis.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["double"],
                            "type": "object",
                            "description": "args: geomA, rotRadians - Rotate a geometry rotRadians about the Y axis.",
                            "properties": {
                                "double": {"format": "precision", "type": "string"}
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_quantile": {
            "post": {
                "tags": ["(rpc) _st_quantile"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rastertable", "rastercolumn"],
                            "type": "object",
                            "properties": {
                                "nband": {"format": "integer", "type": "integer"},
                                "sample_percent": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "rastertable": {"format": "text", "type": "string"},
                                "exclude_nodata_value": {
                                    "format": "boolean",
                                    "type": "boolean",
                                },
                                "quantiles": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "rastercolumn": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_st_asgeojson": {
            "post": {
                "tags": ["(rpc) _st_asgeojson"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/_add_raster_constraint": {
            "post": {
                "tags": ["(rpc) _add_raster_constraint"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["cn", "sql"],
                            "type": "object",
                            "properties": {
                                "cn": {"format": "name", "type": "string"},
                                "sql": {"format": "text", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/longtransactionsenabled": {
            "post": {
                "tags": ["(rpc) longtransactionsenabled"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/postgis_lib_version": {
            "post": {
                "tags": ["(rpc) postgis_lib_version"],
                "summary": "Returns the version number of the PostGIS library.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "Returns the version number of the PostGIS library.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geography_in": {
            "post": {
                "tags": ["(rpc) geography_in"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_boundary": {
            "post": {
                "tags": ["(rpc) st_boundary"],
                "summary": "args: geomA - Returns the closure of the combinatorial boundary of this Geometry.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: geomA - Returns the closure of the combinatorial boundary of this Geometry.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_gist_compress_nd": {
            "post": {
                "tags": ["(rpc) geometry_gist_compress_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_mindist4ma": {
            "post": {
                "tags": ["(rpc) st_mindist4ma"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["value", "pos"],
                            "type": "object",
                            "properties": {
                                "value": {
                                    "format": "double precision[]",
                                    "type": "string",
                                },
                                "pos": {"format": "integer[]", "type": "string"},
                                "VARIADIC": {
                                    "format": "userargs text[]",
                                    "type": "string",
                                },
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/geometry_overlaps_nd": {
            "post": {
                "tags": ["(rpc) geometry_overlaps_nd"],
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {"type": "object"},
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_reverse": {
            "post": {
                "tags": ["(rpc) st_reverse"],
                "summary": "args: g1 - Return the geometry with vertex order reversed.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g1 - Return the geometry with vertex order reversed.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_addband": {
            "post": {
                "tags": ["(rpc) st_addband"],
                "summary": "args: rast, outdbfile, outdbindex, index=at_end, nodataval=NULL - Returns a raster with the new band(s) of given type added with given initial value in the given index location. If no index is specified, the band is added to the end.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["rast", "outdbfile", "outdbindex"],
                            "type": "object",
                            "description": "args: rast, outdbfile, outdbindex, index=at_end, nodataval=NULL - Returns a raster with the new band(s) of given type added with given initial value in the given index location. If no index is specified, the band is added to the end.",
                            "properties": {
                                "rast": {"format": "raster", "type": "string"},
                                "nodataval": {
                                    "format": "double precision",
                                    "type": "number",
                                },
                                "index": {"format": "integer", "type": "integer"},
                                "outdbfile": {"format": "text", "type": "string"},
                                "outdbindex": {"format": "integer[]", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_x": {
            "post": {
                "tags": ["(rpc) st_x"],
                "summary": "args: a_point - Return the X coordinate of the point, or NULL if not available. Input must be a point.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: a_point - Return the X coordinate of the point, or NULL if not available. Input must be a point.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_crosses": {
            "post": {
                "tags": ["(rpc) st_crosses"],
                "summary": "args: g1, g2 - Returns TRUE if the supplied geometries have some, but not all, interior points in common.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "required": ["geom1", "geom2"],
                            "type": "object",
                            "description": "args: g1, g2 - Returns TRUE if the supplied geometries have some, but not all, interior points in common.",
                            "properties": {
                                "geom1": {"format": "geometry", "type": "string"},
                                "geom2": {"format": "geometry", "type": "string"},
                            },
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
        "/rpc/st_isring": {
            "post": {
                "tags": ["(rpc) st_isring"],
                "summary": "args: g - Returns TRUE if this LINESTRING is both closed and simple.",
                "produces": ["application/json", "application/vnd.pgrst.object+json"],
                "parameters": [
                    {
                        "required": true,
                        "schema": {
                            "type": "object",
                            "description": "args: g - Returns TRUE if this LINESTRING is both closed and simple.",
                        },
                        "in": "body",
                        "name": "args",
                    },
                    {"$ref": "#/parameters/preferParams"},
                ],
                "responses": {"200": {"description": "OK"}},
            }
        },
    },
    "definitions": {
        "datacite": {
            "properties": {"data": {"format": "json", "type": "string"}},
            "type": "object",
        },
        "dataset_list": {
            "properties": {
                "ds_id": {
                    "format": "integer",
                    "type": "integer",
                    "description": "Note:\nThis is a Primary Key.<pk/>",
                },
                "title": {"format": "text", "type": "string"},
                "is_raster": {"format": "boolean", "type": "boolean"},
                "is_tiled": {"format": "boolean", "type": "boolean"},
                "shared_id": {
                    "maxLength": 200,
                    "format": "character varying",
                    "type": "string",
                },
                "group": {"format": "text", "type": "string"},
            },
            "type": "object",
        },
        "datasets": {
            "required": ["ds_id"],
            "properties": {
                "ds_id": {
                    "format": "integer",
                    "type": "integer",
                    "description": "Note:\nThis is a Primary Key.<pk/>",
                },
                "metadata": {"format": "jsonb", "type": "string"},
                "shared_id": {
                    "maxLength": 200,
                    "format": "character varying",
                    "type": "string",
                },
            },
            "type": "object",
        },
        "geography_columns": {
            "properties": {
                "f_table_catalog": {"format": "name", "type": "string"},
                "f_table_schema": {"format": "name", "type": "string"},
                "f_table_name": {"format": "name", "type": "string"},
                "f_geography_column": {"format": "name", "type": "string"},
                "coord_dimension": {"format": "integer", "type": "integer"},
                "srid": {"format": "integer", "type": "integer"},
                "type": {"format": "text", "type": "string"},
            },
            "type": "object",
        },
        "geometry_columns": {
            "properties": {
                "f_table_catalog": {
                    "maxLength": 256,
                    "format": "character varying",
                    "type": "string",
                },
                "f_table_schema": {"format": "name", "type": "string"},
                "f_table_name": {"format": "name", "type": "string"},
                "f_geometry_column": {"format": "name", "type": "string"},
                "coord_dimension": {"format": "integer", "type": "integer"},
                "srid": {"format": "integer", "type": "integer"},
                "type": {
                    "maxLength": 30,
                    "format": "character varying",
                    "type": "string",
                },
            },
            "type": "object",
        },
        "metadata": {
            "properties": {
                "ds_id": {
                    "format": "integer",
                    "type": "integer",
                    "description": "Note:\nThis is a Primary Key.<pk/>",
                },
                "shared_id": {
                    "maxLength": 200,
                    "format": "character varying",
                    "type": "string",
                },
                "metadata": {"format": "json", "type": "string"},
            },
            "type": "object",
        },
        "parameters": {
            "properties": {
                "ds_id": {
                    "format": "integer",
                    "type": "integer",
                    "description": "Note:\nThis is a Primary Key.<pk/>",
                },
                "title": {"format": "text", "type": "string"},
                "variables": {"format": "text", "type": "string"},
                "start_at": {"format": "timestamp without time zone", "type": "string"},
                "end_at": {"format": "timestamp without time zone", "type": "string"},
                "fields": {"format": "jsonb", "type": "string"},
                "is_raster": {"format": "boolean", "type": "boolean"},
                "temporal_granularity": {"format": "text", "type": "string"},
                "time_periods": {"format": "jsonb", "type": "string"},
                "is_tiled": {"format": "boolean", "type": "boolean"},
                "levels": {"format": "jsonb", "type": "string"},
                "default_parameters": {"format": "jsonb", "type": "string"},
            },
            "type": "object",
        },
        "raster_columns": {
            "properties": {
                "r_table_catalog": {"format": "name", "type": "string"},
                "r_table_schema": {"format": "name", "type": "string"},
                "r_table_name": {"format": "name", "type": "string"},
                "r_raster_column": {"format": "name", "type": "string"},
                "srid": {"format": "integer", "type": "integer"},
                "scale_x": {"format": "double precision", "type": "number"},
                "scale_y": {"format": "double precision", "type": "number"},
                "blocksize_x": {"format": "integer", "type": "integer"},
                "blocksize_y": {"format": "integer", "type": "integer"},
                "same_alignment": {"format": "boolean", "type": "boolean"},
                "regular_blocking": {"format": "boolean", "type": "boolean"},
                "num_bands": {"format": "integer", "type": "integer"},
                "pixel_types": {"format": "ARRAY", "type": "string"},
                "nodata_values": {"format": "ARRAY", "type": "string"},
                "out_db": {"format": "ARRAY", "type": "string"},
                "extent": {"format": "public.geometry", "type": "string"},
                "spatial_index": {"format": "boolean", "type": "boolean"},
            },
            "type": "object",
        },
        "raster_overviews": {
            "properties": {
                "o_table_catalog": {"format": "name", "type": "string"},
                "o_table_schema": {"format": "name", "type": "string"},
                "o_table_name": {"format": "name", "type": "string"},
                "o_raster_column": {"format": "name", "type": "string"},
                "r_table_catalog": {"format": "name", "type": "string"},
                "r_table_schema": {"format": "name", "type": "string"},
                "r_table_name": {"format": "name", "type": "string"},
                "r_raster_column": {"format": "name", "type": "string"},
                "overview_factor": {"format": "integer", "type": "integer"},
            },
            "type": "object",
        },
        "spatial_ref_sys": {
            "required": ["srid"],
            "properties": {
                "srid": {
                    "format": "integer",
                    "type": "integer",
                    "description": "Note:\nThis is a Primary Key.<pk/>",
                },
                "auth_name": {
                    "maxLength": 256,
                    "format": "character varying",
                    "type": "string",
                },
                "auth_srid": {"format": "integer", "type": "integer"},
                "srtext": {
                    "maxLength": 2048,
                    "format": "character varying",
                    "type": "string",
                },
                "proj4text": {
                    "maxLength": 2048,
                    "format": "character varying",
                    "type": "string",
                },
            },
            "type": "object",
        },
    },
    "parameters": {
        "preferParams": {
            "name": "Prefer",
            "description": "Preference",
            "required": false,
            "in": "header",
            "type": "string",
            "enum": ["params=single-object"],
        },
        "preferReturn": {
            "name": "Prefer",
            "description": "Preference",
            "required": false,
            "in": "header",
            "type": "string",
            "enum": ["return=representation", "return=minimal", "return=none"],
        },
        "preferCount": {
            "name": "Prefer",
            "description": "Preference",
            "required": false,
            "in": "header",
            "type": "string",
            "enum": ["count=none"],
        },
        "select": {
            "name": "select",
            "description": "Filtering Columns",
            "required": false,
            "in": "query",
            "type": "string",
        },
        "on_conflict": {
            "name": "on_conflict",
            "description": "On Conflict",
            "required": false,
            "in": "query",
            "type": "string",
        },
        "order": {
            "name": "order",
            "description": "Ordering",
            "required": false,
            "in": "query",
            "type": "string",
        },
        "range": {
            "name": "Range",
            "description": "Limiting and Pagination",
            "required": false,
            "in": "header",
            "type": "string",
        },
        "rangeUnit": {
            "name": "Range-Unit",
            "description": "Limiting and Pagination",
            "required": false,
            "default": "items",
            "in": "header",
            "type": "string",
        },
        "offset": {
            "name": "offset",
            "description": "Limiting and Pagination",
            "required": false,
            "in": "query",
            "type": "string",
        },
        "limit": {
            "name": "limit",
            "description": "Limiting and Pagination",
            "required": false,
            "in": "query",
            "type": "string",
        },
        "body.datacite": {
            "name": "datacite",
            "description": "datacite",
            "required": false,
            "schema": {"$ref": "#/definitions/datacite"},
            "in": "body",
        },
        "rowFilter.datacite.data": {
            "name": "data",
            "required": false,
            "format": "json",
            "in": "query",
            "type": "string",
        },
        "body.dataset_list": {
            "name": "dataset_list",
            "description": "dataset_list",
            "required": false,
            "schema": {"$ref": "#/definitions/dataset_list"},
            "in": "body",
        },
        "rowFilter.dataset_list.ds_id": {
            "name": "ds_id",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.dataset_list.title": {
            "name": "title",
            "required": false,
            "format": "text",
            "in": "query",
            "type": "string",
        },
        "rowFilter.dataset_list.is_raster": {
            "name": "is_raster",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "rowFilter.dataset_list.is_tiled": {
            "name": "is_tiled",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "rowFilter.dataset_list.shared_id": {
            "name": "shared_id",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "rowFilter.dataset_list.group": {
            "name": "group",
            "required": false,
            "format": "text",
            "in": "query",
            "type": "string",
        },
        "body.datasets": {
            "name": "datasets",
            "description": "datasets",
            "required": false,
            "schema": {"$ref": "#/definitions/datasets"},
            "in": "body",
        },
        "rowFilter.datasets.ds_id": {
            "name": "ds_id",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.datasets.metadata": {
            "name": "metadata",
            "required": false,
            "format": "jsonb",
            "in": "query",
            "type": "string",
        },
        "rowFilter.datasets.shared_id": {
            "name": "shared_id",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "body.geography_columns": {
            "name": "geography_columns",
            "description": "geography_columns",
            "required": false,
            "schema": {"$ref": "#/definitions/geography_columns"},
            "in": "body",
        },
        "rowFilter.geography_columns.f_table_catalog": {
            "name": "f_table_catalog",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geography_columns.f_table_schema": {
            "name": "f_table_schema",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geography_columns.f_table_name": {
            "name": "f_table_name",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geography_columns.f_geography_column": {
            "name": "f_geography_column",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geography_columns.coord_dimension": {
            "name": "coord_dimension",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geography_columns.srid": {
            "name": "srid",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geography_columns.type": {
            "name": "type",
            "required": false,
            "format": "text",
            "in": "query",
            "type": "string",
        },
        "body.geometry_columns": {
            "name": "geometry_columns",
            "description": "geometry_columns",
            "required": false,
            "schema": {"$ref": "#/definitions/geometry_columns"},
            "in": "body",
        },
        "rowFilter.geometry_columns.f_table_catalog": {
            "name": "f_table_catalog",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geometry_columns.f_table_schema": {
            "name": "f_table_schema",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geometry_columns.f_table_name": {
            "name": "f_table_name",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geometry_columns.f_geometry_column": {
            "name": "f_geometry_column",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geometry_columns.coord_dimension": {
            "name": "coord_dimension",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geometry_columns.srid": {
            "name": "srid",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.geometry_columns.type": {
            "name": "type",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "body.metadata": {
            "name": "metadata",
            "description": "metadata",
            "required": false,
            "schema": {"$ref": "#/definitions/metadata"},
            "in": "body",
        },
        "rowFilter.metadata.ds_id": {
            "name": "ds_id",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.metadata.shared_id": {
            "name": "shared_id",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "rowFilter.metadata.metadata": {
            "name": "metadata",
            "required": false,
            "format": "json",
            "in": "query",
            "type": "string",
        },
        "body.parameters": {
            "name": "parameters",
            "description": "parameters",
            "required": false,
            "schema": {"$ref": "#/definitions/parameters"},
            "in": "body",
        },
        "rowFilter.parameters.ds_id": {
            "name": "ds_id",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.title": {
            "name": "title",
            "required": false,
            "format": "text",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.variables": {
            "name": "variables",
            "required": false,
            "format": "text",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.start_at": {
            "name": "start_at",
            "required": false,
            "format": "timestamp without time zone",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.end_at": {
            "name": "end_at",
            "required": false,
            "format": "timestamp without time zone",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.fields": {
            "name": "fields",
            "required": false,
            "format": "jsonb",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.is_raster": {
            "name": "is_raster",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.temporal_granularity": {
            "name": "temporal_granularity",
            "required": false,
            "format": "text",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.time_periods": {
            "name": "time_periods",
            "required": false,
            "format": "jsonb",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.is_tiled": {
            "name": "is_tiled",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.levels": {
            "name": "levels",
            "required": false,
            "format": "jsonb",
            "in": "query",
            "type": "string",
        },
        "rowFilter.parameters.default_parameters": {
            "name": "default_parameters",
            "required": false,
            "format": "jsonb",
            "in": "query",
            "type": "string",
        },
        "body.raster_columns": {
            "name": "raster_columns",
            "description": "raster_columns",
            "required": false,
            "schema": {"$ref": "#/definitions/raster_columns"},
            "in": "body",
        },
        "rowFilter.raster_columns.r_table_catalog": {
            "name": "r_table_catalog",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.r_table_schema": {
            "name": "r_table_schema",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.r_table_name": {
            "name": "r_table_name",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.r_raster_column": {
            "name": "r_raster_column",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.srid": {
            "name": "srid",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.scale_x": {
            "name": "scale_x",
            "required": false,
            "format": "double precision",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.scale_y": {
            "name": "scale_y",
            "required": false,
            "format": "double precision",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.blocksize_x": {
            "name": "blocksize_x",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.blocksize_y": {
            "name": "blocksize_y",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.same_alignment": {
            "name": "same_alignment",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.regular_blocking": {
            "name": "regular_blocking",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.num_bands": {
            "name": "num_bands",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.pixel_types": {
            "name": "pixel_types",
            "required": false,
            "format": "ARRAY",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.nodata_values": {
            "name": "nodata_values",
            "required": false,
            "format": "ARRAY",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.out_db": {
            "name": "out_db",
            "required": false,
            "format": "ARRAY",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.extent": {
            "name": "extent",
            "required": false,
            "format": "public.geometry",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_columns.spatial_index": {
            "name": "spatial_index",
            "required": false,
            "format": "boolean",
            "in": "query",
            "type": "string",
        },
        "body.raster_overviews": {
            "name": "raster_overviews",
            "description": "raster_overviews",
            "required": false,
            "schema": {"$ref": "#/definitions/raster_overviews"},
            "in": "body",
        },
        "rowFilter.raster_overviews.o_table_catalog": {
            "name": "o_table_catalog",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.o_table_schema": {
            "name": "o_table_schema",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.o_table_name": {
            "name": "o_table_name",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.o_raster_column": {
            "name": "o_raster_column",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.r_table_catalog": {
            "name": "r_table_catalog",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.r_table_schema": {
            "name": "r_table_schema",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.r_table_name": {
            "name": "r_table_name",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.r_raster_column": {
            "name": "r_raster_column",
            "required": false,
            "format": "name",
            "in": "query",
            "type": "string",
        },
        "rowFilter.raster_overviews.overview_factor": {
            "name": "overview_factor",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "body.spatial_ref_sys": {
            "name": "spatial_ref_sys",
            "description": "spatial_ref_sys",
            "required": false,
            "schema": {"$ref": "#/definitions/spatial_ref_sys"},
            "in": "body",
        },
        "rowFilter.spatial_ref_sys.srid": {
            "name": "srid",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.spatial_ref_sys.auth_name": {
            "name": "auth_name",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "rowFilter.spatial_ref_sys.auth_srid": {
            "name": "auth_srid",
            "required": false,
            "format": "integer",
            "in": "query",
            "type": "string",
        },
        "rowFilter.spatial_ref_sys.srtext": {
            "name": "srtext",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
        "rowFilter.spatial_ref_sys.proj4text": {
            "name": "proj4text",
            "required": false,
            "format": "character varying",
            "in": "query",
            "type": "string",
        },
    },
    "externalDocs": {
        "url": "https://postgrest.org/en/v7.0/api.html",
        "description": "PostgREST Documentation",
    },
}
