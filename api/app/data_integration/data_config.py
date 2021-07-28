from app.data_integration.ds_colors import COLORS

DATASETS_DIC = {
    "DS_1": {
        "id": 1,
        "layer_type": "raster",
        "params": """{
            "data.ds_id":1,
            "variable":"''Monthly average global irradiance on a horizontal surface (W/m2), period 2005-2015''",
            "start_at":"''01-01-2099  00:00:00''"}""",
        "json_params": {
            "parameters": {
                "data.ds_id": 1,
                "variable": "'Monthly average global irradiance on a horizontal surface (W/m2), period 2005-2015'",
                "start_at": "'01-01-2099  00:00:00'",
            },
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_2": {
        "id": 2,
        "layer_type": "vector",
        "params": """{"data.ds_id":2}""",
        "json_params": {"parameters": {"data.ds_id": 2}, "row_limit": 100000},
        "title": "",
        "legend": {
            "legend_variable": {"variable": "gross_cap_ele", "min": 0.0, "max": 275.0}
        },
    },
    "DS_3": {
        "id": 3,
        "layer_type": "vector",
        "params": """{"data.ds_id":3}""",
        "json_params": {"parameters": {"data.ds_id": 3}, "row_limit": 100000},
        "title": "",
        "legend": {
            "legend_variable": {
                "variable": "installed_capacity_MW",
                "min": 0.0,
                "max": 2070.0,
            }
        },
    },
    "DS_4": {
        "id": 4,
        "layer_type": "vector",
        "params": """{"data.ds_id":4}""",
        "json_params": {"parameters": {"data.ds_id": 4}, "row_limit": 100000},
        "title": "",
        "legend": {
            "legend_variable": {"variable": "capacity_g", "min": 0.0, "max": 4690.0}
        },
    },
    "DS_5": {
        "id": 5,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":5,
                        "start_at":"''01/01/2019  00:00:00''",
                        "fields":{
                            "Market_Sector":"Total"
                        }
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 5,
                "start_at": "'01/01/2019  00:00:00'",
                "fields": {"Market_Sector": "Total"},
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["green"]},
            "legend_variable": {"variable": "Total", "min": 0.05, "max": 0.56},
        },
    },
    "DS_6": {
        "id": 6,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":6,
                        "start_at":"''01/01/2010  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 6, "start_at": "'01/01/2010  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["blue"]},
            "legend_variable": {
                "variable": "Electricity : Final consumption - other sectors - households - energy use",
                "min": 815,
                "max": 161520,
            },
        },
    },
    "DS_9": {
        "id": 9,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":9,
                        "start_at":"''01/01/2010  00:00:00''",
                        "level": " { country } "
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 9,
                "start_at": "'01/01/2010  00:00:00'",
                "level": "{ country }",
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "legend_variable": {
                "variable": "Heating degree days",
                "min": 124.0,
                "max": 1022.0,
            }
        },
    },
    "DS_11": {
        "id": 11,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":11,
                        "start_at":"''01/01/2010  00:00:00''",
                        "fields":{
                            "action":"Renewable energy technologies"
                        }
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 11,
                "start_at": "'01/01/2010  00:00:00'",
                "fields": {"action": "Renewable energy technologies"},
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "legend_variable": {"variable": "inventions", "min": 0.0, "max": 844.0}
        },
    },
    "DS_15": {
        "id": 15,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":15,
                        "start_at":"''01/01/2018  00:00:00''",
                        "variable":"''10m_u_component_of_wind''"
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 15,
                "start_at": "'01/01/2018  00:00:00'",
                "variable": "'10m_u_component_of_wind'",
            },
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_16": {
        "id": 16,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":16,
                        "start_at":"''01/01/2014  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 16, "start_at": "'01/01/2014  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["green"]},
            "legend_variable": {
                "variable": "installed wind power capacity",
                "min": 0.0,
                "max": 1.0,
            },
        },
    },
    "DS_17": {
        "id": 17,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":17,
                        "start_at":"''01/01/2014  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 17, "start_at": "'01/01/2014  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["pink"]},
            "legend_variable": {
                "variable": "installed PV power capacity",
                "min": 0.0,
                "max": 0.0,
            },
        },
    },
    "DS_18": {
        "id": 18,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":18,
                        "start_at":"''01/01/2012  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 18, "start_at": "'01/01/2012  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["violet"]},
            "legend_variable": {
                "variable": "Energy intensity level of primary energy ",
                "min": 0.39,
                "max": 42.0,
            },
        },
    },
    "DS_19": {
        "id": 19,
        "layer_type": "vector",
        "params": """{
                    "data.ds_id":19,
                    "start_at":"''01/01/2012  00:00:00''",
                    "fields":{
                        "Sector":"Power Industry"
                    }
                }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 19,
                "start_at": "'01/01/2012  00:00:00'",
                "fields": {"Sector": "Power Industry"},
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "legend_variable": {"variable": "Emissions", "min": 0.0, "max": 4155}
        },
    },
    "DS_20": {
        "id": 20,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":20,
                        "start_at":"''01/01/2019  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 20, "start_at": "'01/01/2019  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_21": {
        "id": 21,
        "layer_type": "raster",
        "params": """{
                            "data.ds_id":21,
                            "intersecting":"POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))"
                        }
                    """,
        "json_params": {
            "parameters": {
                "data.ds_id": 21,
                "intersecting": "POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))",
            },
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_22": {
        "id": 22,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":22,
                        "start_at":"''01/01/2018  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 22, "start_at": "'01/01/2018  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "legend_variable": {
                "variable": "Final energy consumption (Europe 2020-2030)",
                "min": 0.65,
                "max": 216.0,
            }
        },
    },
    "DS_24": {
        "id": 24,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":24,
                        "start_at":"''01/01/2099  00:00:00''",
                        "intersecting":"POLYGON((10.276722801998659 48.889240956946985,10.2747270124557986 48.835409141414466,10.390482805942611 48.847230841511724,10.3445796464564523 48.91023278929048,10.276722801998659 48.889240956946985))"
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 24,
                "start_at": "'01/01/2099  00:00:00'",
                "intersecting": "POLYGON((10.276722801998659 48.889240956946985,10.2747270124557986 48.835409141414466,10.390482805942611 48.847230841511724,10.3445796464564523 48.91023278929048,10.276722801998659 48.889240956946985))",
            },
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_27": {
        "id": 27,
        "layer_type": "vector",
        "params": """{
                    "data.ds_id":27,
                    "start_at":"''01/01/2012  00:00:00''",
                    "fields":{
                        "parameter":"Dry Mass",
                        "potential":"Base potential"
                    }
                }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 27,
                "start_at": "'01/01/2012  00:00:00'",
                "fields": {"parameter": "Dry Mass", "potential": "Base potential"},
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["orange"]},
            "legend_variable": {
                "variable": "Base potential : Bark residues from pulp and paper industry",
                "min": 0.0,
                "max": 216.0,
            },
        },
    },
    "DS_28": {
        "id": 28,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":28,
                        "start_at":"''01/01/1945  00:00:00''",
                        "fields":{
                            "bage":"1945 - 1969",
                            "btype":"Single family- Terraced houses",
                            "detail":"insulation",
                            "sector":"Residential sector"
                        }
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 28,
                "start_at": "'01/01/1945  00:00:00'",
                "fields": {
                    "bage": "1945 - 1969",
                    "btype": "Single family- Terraced houses",
                    "detail": "insulation",
                    "sector": "Residential sector",
                },
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["blue"]},
            "legend_variable": {
                "variable": "ROOF | construction material | None",
                "min": 0.66,
                "max": 1.0,
            },
        },
    },
    "DS_29": {
        "id": 29,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":29,
                        "start_at":"''2012-01-01''",
                        "fields":{
                            "Fuel":"gas",
                            "Type":"space heating",
                            "Scenario":"current",
                            "Supertype":"Residential",
                            "Technology":"Gas boiler or stove"
                        }
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 29,
                "start_at": "'2012-01-01'",
                "fields": {
                    "Fuel": "gas",
                    "Type": "space heating",
                    "Scenario": "current",
                    "Supertype": "Residential",
                    "Technology": "Gas boiler or stove",
                },
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["green"]},
            "legend_variable": {
                "variable": "final energy demand",
                "min": 0.0,
                "max": 237713.0,
            },
        },
    },
    "DS_30": {
        "id": 30,
        "layer_type": "vector",
        "params": """{
                    "data.ds_id":30,
                    "start_at":"''2012-01-01''",
                    "fields":{
                        "Sector":"Industry",
                        "Scenario":"CP",
                        "Sub-sector":"TOTAL Industry",
                        "Energy type":"Final Energy",
                        "Energy Carrier":"Total"
                    }
                }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 30,
                "start_at": "'2012-01-01'",
                "fields": {
                    "Sector": "Industry",
                    "Scenario": "CP",
                    "Sub-sector": "TOTAL Industry",
                    "Energy type": "Final Energy",
                    "Energy Carrier": "Total",
                },
            },
            "row_limit": 100000,
        },
        "legend": {
            "style": {"colors": COLORS["red"]},
            "legend_variable": {
                "variable": "Final Energy | Heating",
                "min": 0.11,
                "max": 504.0,
            },
        },
    },
    "DS_31": {
        "id": 31,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":31,
                        "variable":"''Climate zones''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 31, "variable": "'Climate zones'"},
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_33": {
        "id": 33,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":33,
                        "intersecting":"POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))"
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 33,
                "intersecting": "POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))",
            },
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_35": {
        "id": 35,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":35,
                        "intersecting":"POLYGON((2.29 48.88,2.29 48.87,2.3 48.87,2.3 48.88,2.29 48.88))"
                    }""",
        "json_params": {
            "parameters": {
                "data.ds_id": 35,
                "intersecting": "POLYGON((2.29 48.88,2.29 48.87,2.3 48.87,2.3 48.88,2.29 48.88))",
            },
            "row_limit": 100000,
        },
        "title": "",
    },
    "DS_42": {
        "id": 42,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":42,
                        "level":" { country } "
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 42, "level": " { country } "},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["green"]},
            "legend_variable": {
                "variable": "Non-residential buildings : Conventional dwellings",
                "min": 0.0,
                "max": 440340.0,
            },
        },
    },
    "DS_43": {
        "id": 43,
        "layer_type": "raster",
        "params": """{
                        "data.ds_id":43
                    }""",
        "json_params": {"parameters": {"data.ds_id": 43}, "row_limit": 100000},
        "title": "",
    },
    "DS_45": {
        "id": 45,
        "layer_type": "raster",
        "params": """{"data.ds_id":45}""",
        "json_params": {"parameters": {"data.ds_id": 45}, "row_limit": 100000},
        "title": "",
    },
    "DS_46": {
        "id": 46,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":46,
                        "start_at":"''2018-01-01''",
                        "fields":{
                            "Pollutant":"Carbon dioxide"
                        }
                    }
                    """,
        "json_params": {
            "parameters": {
                "data.ds_id": 46,
                "start_at": "'2018-01-01'",
                "fields": {"Pollutant": "Carbon dioxide"},
            },
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["pink"]},
            "legend_variable": {
                "variable": "Total  emissions excluding LULUCF | Carbon dioxide",
                "min": 3675.0,
                "max": 5424882.0,
            },
        },
    },
    "DS_47": {
        "id": 47,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":47,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 47, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["orange"]},
            "legend_variable": {
                "variable": "Band DA : Consumption < 1 000 kWh : All taxes and levies included",
                "min": -0.027,
                "max": 0.6,
            },
        },
    },
    "DS_48": {
        "id": 48,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":48,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 48, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["green"]},
            "legend_variable": {
                "variable": "Electricity, gas and other fuels",
                "min": 130.0,
                "max": 66265.0,
            },
        },
    },
    "DS_49": {
        "id": 49,
        "layer_type": "vector",
        "params": """{
                        "data.ds_id":49,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 49, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["violet"]},
            "legend_variable": {
                "variable": "Natural gas",
                "min": -1822.0,
                "max": 110.0,
            },
        },
    },
    "DS_50": {
        "id": 50,
        "layer_type": "vector",
        "params": """{
                    "data.ds_id":50,
                    "start_at":"''2018-01-01''"
                }""",
        "json_params": {
            "parameters": {"data.ds_id": 50, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "",
        "legend": {
            "style": {"colors": COLORS["orange"]},
            "legend_variable": {"variable": "default", "min": 1038.0, "max": 651258.0},
        },
    },
}


def get_ds_title(dataset_id):
    dataset_params = get_ds(dataset_id)
    title = dataset_params.get("title", None)
    if title is None or not title:
        return "undefined"
    return title


def get_ds_ids():
    ids = []
    for value in DATASETS_DIC.values():
        id = value.get("id", None)
        if id:
            ids.append(id)
    return ids


def get_ds(dataset_id):
    """Return the dataset default parameters in a dict or an
    empty dict if there is no default parameters for this dataset"""
    for value in DATASETS_DIC.values():
        if value.get("id", None) == dataset_id:
            return value
    else:
        return {}


def get_legend_style(dataset_id):
    """Get the style used to color the map or a default style if the
    legend or the style are undefined"""
    default_style = {
        "colors": COLORS["red"],
    }
    dataset_params = get_ds(dataset_id)
    legend = dataset_params.get("legend", None)
    if legend is not None:
        style = legend.get("style", None)
        if style is not None:
            return style
    # If there is no legend or style defined, return default style
    return default_style


def get_legend_variable(dataset_id):
    """
    Return the variable used to color the layer and its min/max values, or
    None if the legend or the variable used to color the map are not specified.
    """
    dataset_params = get_ds(dataset_id)
    legend = dataset_params.get("legend", None)
    if legend is not None:
        return legend.get("legend_variable", None)
