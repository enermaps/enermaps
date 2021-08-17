DATASETS_DIC = {
    "DS_1": {
        "id": 1,
        "layer_type": "raster",
        "data_type": "numerical",
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
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Monthly average global irradiance on a horizontal surface (W/m2), period 2005-2015: W/m2",
                "units": "W/m2",
                "min": 13.9,
                "max": 284.6,
            },
        },
        "title": "PVGIS: Solar Radiation Data",
        "openair_link": "",
    },
    "DS_2": {
        "id": 2,
        "layer_type": "vector",
        "data_type": "point",
        "params": """{"data.ds_id":2}""",
        "json_params": {"parameters": {"data.ds_id": 2}, "row_limit": 100000},
        "title": "JRC: Geothermal Power Plant Dataset",
        "legend": {
            "legend_variable": {
                "variable": "gross_cap_ele",
                "units": "MW",
                "min": 0.0,
                "max": 275.0,
            }
        },
    },
    "DS_3": {
        "id": 3,
        "layer_type": "vector",
        "data_type": "point",
        "params": """{"data.ds_id":3}""",
        "json_params": {"parameters": {"data.ds_id": 3}, "row_limit": 100000},
        "title": "JRC: Hydro-power plants database",
        "legend": {
            "legend_variable": {
                "variable": "installed_capacity_MW",
                "units": "MW",
                "min": 0.0,
                "max": 2070.0,
            }
        },
    },
    "DS_4": {
        "id": 4,
        "layer_type": "vector",
        "data_type": "point",
        "params": """{"data.ds_id":4}""",
        "json_params": {"parameters": {"data.ds_id": 4}, "row_limit": 100000},
        "title": "JRC: Open Power Plants Database",
        "legend": {
            "legend_variable": {
                "variable": "capacity_g",
                "units": "MW",
                "min": 0.0,
                "max": 4690.0,
            }
        },
    },
    "DS_5": {
        "id": 5,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "EEA: Share of gross final consumption of renewable energy sources",
        "legend": {
            "style": {"colors": {"color_palet": "crest", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Total",
                "units": "%",
                "min": 0.05,
                "max": 0.56,
            },
        },
    },
    "DS_6": {
        "id": 6,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":6,
                        "start_at":"''01/01/2010  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 6, "start_at": "'01/01/2010  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "Energy consumption in households",
        "legend": {
            "style": {"colors": {"color_palet": "magma", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Electricity : Final consumption - other sectors - households - energy use",
                "units": "Gigawatt-hour",
                "min": 815,
                "max": 161520,
            },
        },
    },
    "DS_9": {
        "id": 9,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "Eurostat: Degree days",
        "legend": {
            "legend_variable": {
                "variable": "Heating degree days",
                "units": "Number",
                "min": 124.0,
                "max": 1022.0,
            }
        },
    },
    "DS_11": {
        "id": 11,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "SETIS: Private R&I investment in energy technologies",
        "legend": {
            "legend_variable": {
                "variable": "inventions",
                "units": "-",
                "min": 0.0,
                "max": 844.0,
            }
        },
    },
    "DS_14": {
        "id": 14,
        "layer_type": "raster",
        "data_type": "numerical",
        "json_params": {
            "parameters": {
                "data.ds_id": 14,
                "start_at": "'01/01/1970 00:00:00'",
                "variable": "'Max 1-day PR'",
            },
            "row_limit": 100000,
        },
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Max 1-day PR",
                "units": "mm",
                "min": 0,
                "max": 875.871,
            },
        },
        "title": "Climate Extreme Indices",
    },
    "DS_15": {
        "id": 15,
        "layer_type": "raster",
        "data_type": "numerical",
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
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "10m_u_component_of_wind",
                "units": "m s**-1",
                "min": -15424,
                "max": 26125,
            },
        },
        "title": "Copernicus: hourly global climate and weather data",
    },
    "DS_16": {
        "id": 16,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":16,
                        "start_at":"''01/01/2014  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 16, "start_at": "'01/01/2014  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "EMHIRES: Wind power generation",
        "legend": {
            "style": {"colors": {"color_palet": "viridis", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "installed wind power capacity",
                "units": "MW",
                "min": 0.0,
                "max": 1.0,
            },
        },
    },
    "DS_17": {
        "id": 17,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":17,
                        "start_at":"''01/01/2014  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 17, "start_at": "'01/01/2014  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "EMHIRES: Solar power generation",
        "legend": {
            "style": {"colors": {"color_palet": "rocket_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "installed PV power capacity",
                "units": "MW",
                "min": None,
                "max": None,
            },
        },
    },
    "DS_18": {
        "id": 18,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":18,
                        "start_at":"''01/01/2012  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 18, "start_at": "'01/01/2012  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "Energy Efficiency Indicator",
        "legend": {
            "style": {"colors": {"color_palet": "light:b", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Energy intensity level of primary energy ",
                "units": "MJ/2011 USD PPP",
                "min": 0.39,
                "max": 42.0,
            },
        },
    },
    "DS_19": {
        "id": 19,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "EDGAR CO_ emissions",
        "legend": {
            "legend_variable": {
                "variable": "Emissions",
                "units": "Mt CO2/year",
                "min": 0.0,
                "max": 4155,
            }
        },
    },
    "DS_20": {
        "id": 20,
        "layer_type": "raster",
        "data_type": "numerical",
        "params": """{
                        "data.ds_id":20,
                        "start_at":"''01/01/2019  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 20, "start_at": "'01/01/2019  00:00:00'"},
            "row_limit": 100000,
        },
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "relative_humidity",
                "units": "%",
                "min": -27093,
                "max": 5119,
            },
        },
        "title": "Copernicus: hourly data on pressure levels",
    },
    "DS_21": {
        "id": 21,
        "layer_type": "raster",
        "data_type": "numerical",
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
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "undefined",
                "units": "undefined",
                "min": 21.7069,
                "max": 165.7,
            },
        },
        "title": "European Digital Elevation Model (EU-DEM)",
    },
    "DS_22": {
        "id": 22,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":22,
                        "start_at":"''01/01/2018  00:00:00''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 22, "start_at": "'01/01/2018  00:00:00'"},
            "row_limit": 100000,
        },
        "title": "Eurostat: Energy efficiency indicator",
        "legend": {
            "legend_variable": {
                "variable": "Final energy consumption (Europe 2020-2030)",
                "units": "Million tonnes of oil equivalent",
                "min": 0.65,
                "max": 216.0,
            }
        },
    },
    "DS_24": {
        "id": 24,
        "layer_type": "raster",
        "data_type": "numerical",
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
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Longterm monthly average of potential photovoltaic electricity production",
                "units": "kWh/kWp",
                "min": 34.224,
                "max": 62.403,
            },
        },
        "title": "Photovoltaic power potential",
    },
    "DS_27": {
        "id": 27,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "S2BIOM: Biomass supply",
        "legend": {
            "style": {"colors": {"color_palet": "dark:salmon_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Base potential : Sawdust from sawmills from conifers",
                "units": "kton dry mass",
                "min": 4.94441691195059,
                "max": 47.5166700166629,
            },
        },
    },
    "DS_28": {
        "id": 28,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "HotMaps: Building stock analysis",
        "legend": {
            "style": {"colors": {"color_palet": "vlag", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "ROOF | construction material | None",
                "units": "dimensionless",
                "min": 0.66,
                "max": 1.0,
            },
        },
    },
    "DS_29": {
        "id": 29,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "H2020 SET-Nav: Detailed scenario results for energy demand by the INVERT-EE-Lab model ",
        "legend": {
            "style": {"colors": {"color_palet": "icefire", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "final energy demand",
                "units": "GWh",
                "min": 0.0,
                "max": 237713.0,
            },
        },
    },
    "DS_30": {
        "id": 30,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "Fuel consumption and technologies used in the heating - cooling sector",
        "legend": {
            "style": {"colors": {"color_palet": "flare", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Final Energy | Heating",
                "units": "TWh",
                "min": 0.11,
                "max": 504.0,
            },
        },
    },
    "DS_31": {
        "id": 31,
        "layer_type": "raster",
        "data_type": "categorical",
        "params": """{
                        "data.ds_id":31,
                        "variable":"''Climate zones''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 31, "variable": "'Climate zones'"},
            "row_limit": 100000,
        },
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Climate zones",
                "units": "-",
                "min": None,
                "max": None,
            },
        },
        "title": "INTERREG GRETA",
    },
    "DS_33": {
        "id": 33,
        "layer_type": "raster",
        "data_type": "numerical",
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
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "undefined",
                "units": "undefined",
                "min": 0,
                "max": 324,
            },
        },
        "title": "Building Height",
    },
    "DS_35": {
        "id": 35,
        "layer_type": "raster",
        "data_type": "numerical",
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
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "undefined",
                "units": "undefined",
                "min": 30,
                "max": 50,
            },
        },
        "title": "European Settlement Map",
    },
    "DS_42": {
        "id": 42,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":42,
                        "level":" { country } "
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 42, "level": " { country } "},
            "row_limit": 100000,
        },
        "title": "National Housing Census: type of living quarter by country",
        "legend": {
            "style": {"colors": {"color_palet": "YlOrBr", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Non-residential buildings : Conventional dwellings",
                "units": "Number",
                "min": 0.0,
                "max": 440340.0,
            },
        },
    },
    "DS_43": {
        "id": 43,
        "layer_type": "raster",
        "data_type": "numerical",
        "params": """{
                        "data.ds_id":43
                    }""",
        "json_params": {"parameters": {"data.ds_id": 43}, "row_limit": 100000},
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Heat density map (final energy demand for heating and DHW) of buildings in EU28 + Switzerland, Norway and Iceland for the year 2015",
                "units": "MWh/ha (MWh/10.000 m2)",
                "min": 0.00142908,
                "max": 3766.61,
            },
        },
        "title": "HotMaps: Heat demand density",
    },
    "DS_45": {
        "id": 45,
        "layer_type": "raster",
        "data_type": "numerical",
        "params": """{"data.ds_id":45}""",
        "json_params": {"parameters": {"data.ds_id": 45}, "row_limit": 100000},
        "legend": {
            "style": {"colors": {"color_palet": "Greys_r", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Heated gross floor area density map of buildings in EU28 + Switzerland, Norway and Iceland for the year 2015",
                "units": "m2/ha (m2/10.000 m2)",
                "min": 0.0111452,
                "max": 33658.4,
            },
        },
        "title": "HotMaps: Heated gross floor area density",
    },
    "DS_46": {
        "id": 46,
        "layer_type": "vector",
        "data_type": "polygon",
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
        "title": "OECD: Greenhouse gas emissions",
        "legend": {
            "style": {"colors": {"color_palet": "Spectral", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Total  emissions excluding LULUCF | Carbon dioxide",
                "units": "Tonnes of CO2 equivalent | Thousands",
                "min": 3675.0,
                "max": 5424882.0,
            },
        },
    },
    "DS_47": {
        "id": 47,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":47,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 47, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "Electricity prices for household consumers",
        "legend": {
            "style": {"colors": {"color_palet": "coolwarm", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Band DA : Consumption < 1 000 kWh : All taxes and levies included",
                "units": "Kilowatt-hour",
                "min": -0.027,
                "max": 0.6,
            },
        },
    },
    "DS_48": {
        "id": 48,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":48,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 48, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "Expenditure per household on energy",
        "legend": {
            "style": {"colors": {"color_palet": "crest", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Electricity, gas and other fuels",
                "units": "Current prices, million euro",
                "min": 130.0,
                "max": 66265.0,
            },
        },
    },
    "DS_49": {
        "id": 49,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                        "data.ds_id":49,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params": {
            "parameters": {"data.ds_id": 49, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "Energy dependence",
        "legend": {
            "style": {"colors": {"color_palet": "viridis", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "Natural gas",
                "units": "Percentage",
                "min": -1822.0,
                "max": 110.0,
            },
        },
    },
    "DS_50": {
        "id": 50,
        "layer_type": "vector",
        "data_type": "polygon",
        "params": """{
                    "data.ds_id":50,
                    "start_at":"''2018-01-01''"
                }""",
        "json_params": {
            "parameters": {"data.ds_id": 50, "start_at": "'2018-01-01'"},
            "row_limit": 100000,
        },
        "title": "Regional GDP",
        "legend": {
            "style": {"colors": {"color_palet": "ch:s=-.2,r=.6", "nb_of_colors": 12}},
            "legend_variable": {
                "variable": "default",
                "units": "Million purchasing power standards (PPS, EU27 from 2020)",
                "min": 1038.0,
                "max": 651258.0,
            },
        },
    },
}
