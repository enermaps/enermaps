
DATASETS_DIC = {
    "DS_1" : {
        "id" : 1,
        "layer_type" : "raster",
        "params" : """{
            "data.ds_id":1,
            "variable":"''Monthly average global irradiance on a horizontal surface (W/m2), period 2005-2015''",
            "start_at":"''01-01-2099  00:00:00''"}""",
        "json_params" : { 
                "parameters" : {
                    "data.ds_id" : 1,
                    "variable" : "'Monthly average global irradiance on a horizontal surface (W/m2), period 2005-2015'",
                    "start_at" : "'01-01-2099  00:00:00'"
                },
                "row_limit" : 100000
            },
        "legend" : "blablabla"
    },
    "DS_2" : {
        "id" : 2,
        "layer_type" : "vector",
        "params" : """{"data.ds_id":2}""",
        "json_params" : {"parameters" : {"data.ds_id":2}, "row_limit" : 100000},
        "legend" : "blablabla"
    },
    "DS_3" : {
        "id" : 3,
        "layer_type" : "vector",
        "params" : """{"data.ds_id":3}""",
        "json_params" : {"parameters" : {"data.ds_id":3}, "row_limit" : 100000},
        "legend" : "blablabla"
    },
    "DS_4" : {
        "id" :  4,
        "layer_type" : "vector",
        "params" : """{"data.ds_id":4}""",
        "json_params" : {"parameters" : {"data.ds_id":4}, "row_limit" : 100000},
        "legend" : "blablabla"
    },
    "DS_5" : {
        "id" : 5,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":5,
                        "start_at":"''01/01/2019  00:00:00''",
                        "fields":{
                            "Market_Sector":"Total"
                        }
                    }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 5,
                    "start_at" : "'01/01/2019  00:00:00'",
                    "fields": {
                        "Market_Sector" : "Total"
                        }
                    },
                "row_limit" : 100000
                },
        "legend" : "blablabla"
    },
    "DS_6" : {
        "id" : 6,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":6,
                        "start_at":"''01/01/2010  00:00:00''"
                    }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 6,
                    "start_at" : "'01/01/2010  00:00:00'"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_9" : {
        "id" : 9,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":9,
                        "start_at":"''01/01/2010  00:00:00''",
                        "level": " { country } "
                    }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 9,
                    "start_at" : "'01/01/2010  00:00:00'",
                    "level" : "{ country }"       
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_11" : {
        "id" : 11,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":11,
                        "start_at":"''01/01/2010  00:00:00''",
                        "fields":{
                            "action":"Renewable energy technologies"
                        }
                    }""",
        "json_params" : {
                "parameters" : {
                        "data.ds_id" : 11,
                        "start_at" : "'01/01/2010  00:00:00'",
                        "fields" : {
                                "action" : "Renewable energy technologies"
                            }
                    },
                "row_limit" : 100000
            },
        "legend" : "blablabla"
    },

    "DS_14" : {
        "id" : 14,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":14,
                        "start_at":"''01/01/1970  00:00:00''",
                        "variable":"''Maximum monthly 1-day precipitation total''"
                    }""",
        "json_params" : {
                "parameters" : {
                        "data.ds_id" : 14,
                        "start_at" : "'01/01/1970  00:00:00'",
                        "variable" : "'Maximum monthly 1-day precipitation total'"
                    },
                "row_limit" : 100000
            },
        "legend" : "blablabla"
    }, 
    "DS_15" : {
        "id" : 15,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":15,
                        "start_at":"''01/01/2018  00:00:00''",
                        "variable":"''10m_u_component_of_wind''"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 15,
                "start_at" : "'01/01/2018  00:00:00'",
                "variable" : "'10m_u_component_of_wind'"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_16" : {
        "id" : 16,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":16,
                        "start_at":"''01/01/2014  00:00:00''"
                    }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 16,
                    "start_at" : "'01/01/2014  00:00:00'"
                },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_17" : {
        "id" : 17,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":17,
                        "start_at":"''01/01/2014  00:00:00''"
                    }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 17,
                    "start_at" : "'01/01/2014  00:00:00'"             
                },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_18" : {
        "id" : 18,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":18,
                        "start_at":"''01/01/2012  00:00:00''"
                    }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 18,
                    "start_at" : "'01/01/2012  00:00:00'"                
                },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },

    "DS_19" : {
        "id" : 19,
        "layer_type" : "vector",
        "params" : """{
                    "data.ds_id":19,
                    "start_at":"''01/01/2012  00:00:00''",
                    "fields":{
                        "Sector":"Power Industry"
                    }
                }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 19,
                "start_at" : "'01/01/2012  00:00:00'",
                "fields" : {
                        "Sector":"Power Industry"
                    }
                },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_20" : {
        "id" : 20,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":20,
                        "start_at":"''01/01/2019  00:00:00''"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id":20,
                "start_at":"'01/01/2019  00:00:00'"                
                },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_21" : {
        "id" : 21,
        "layer_type" : "raster",
        "params" : """{
                            "data.ds_id":21,
                            "intersecting":"POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))"
                        }
                    """,
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 21,
                "intersecting" : "POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_22" : {
        "id" : 22,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":22,
                        "start_at":"''01/01/2018  00:00:00''"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 22,
                "start_at" : "'01/01/2018  00:00:00'"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_24" : {
        "id" : 24,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":24,
                        "start_at":"''01/01/2099  00:00:00''",
                        "intersecting":"POLYGON((10.276722801998659 48.889240956946985,10.2747270124557986 48.835409141414466,10.390482805942611 48.847230841511724,10.3445796464564523 48.91023278929048,10.276722801998659 48.889240956946985))"
                    }""",
        "json_params" : {
            "parameters": {
                "data.ds_id" : 24,
                "start_at" : "'01/01/2099  00:00:00'",
                "intersecting" : "POLYGON((10.276722801998659 48.889240956946985,10.2747270124557986 48.835409141414466,10.390482805942611 48.847230841511724,10.3445796464564523 48.91023278929048,10.276722801998659 48.889240956946985))"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_27" : {
        "id" : 27,
        "layer_type" : "vector",
        "params" : """{
                    "data.ds_id":27,
                    "start_at":"''01/01/2012  00:00:00''",
                    "fields":{
                        "parameter":"Dry Mass",
                        "potential":"Base potential"
                    }
                }""",
        "json_params" : {
            "parameters" : {
                    "data.ds_id" : 27,
                    "start_at" : "'01/01/2012  00:00:00'",
                    "fields" : {
                        "parameter" : "Dry Mass",
                        "potential" : "Base potential"
                    }
            },
            "row_limit" : 100000
        },
        "legend" : "blablalaa"
    },
    "DS_28" : {
        "id" : 28,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":28,
                        "start_at":"''01/01/1945  00:00:00''",
                        "fields":{
                            "bage":"1945 - 1969",
                            "btype":"Single family- Terraced houses",
                            "detail":"insulation",
                            "sector":"Residential sector"
                        }
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 28,
                "start_at" : "'01/01/1945  00:00:00'",
                "fields" : {
                    "bage" : "1945 - 1969",
                    "btype" : "Single family- Terraced houses",
                    "detail" : "insulation",
                    "sector" : "Residential sector"
                }
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_29" : {
        "id" : 29,
        "layer_type" : "vector",
        "params" : """{
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
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 29,
                "start_at" : "'2012-01-01'",
                "fields" : {
                    "Fuel" : "gas",
                    "Type" : "space heating",
                    "Scenario" : "current",
                    "Supertype" : "Residential",
                    "Technology" : "Gas boiler or stove"
                }
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_30" : {
        "id" : 30,
        "layer_type" : "vector",
        "params" : """{
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
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 30,
                "start_at" : "'2012-01-01'",
                "fields" : {
                    "Sector":"Industry",
                    "Scenario":"CP",
                    "Sub-sector":"TOTAL Industry",
                    "Energy type":"Final Energy",
                    "Energy Carrier":"Total"
                }
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_31" : {
        "id" : 31,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":31,
                        "variable":"''Climate zones''"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 31,
                "variable" : "'Climate zones'"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_33" : {
        "id" : 33,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":33,
                        "intersecting":"POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 33,
                "intersecting" : "POLYGON((2.276722801998659 48.889240956946985,2.2747270124557986 48.835409141414466,2.390482805942611 48.847230841511724,2.3445796464564523 48.91023278929048,2.276722801998659 48.889240956946985))"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_35" : {
        "id" : 35,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":35,
                        "intersecting":"POLYGON((2.29 48.88,2.29 48.87,2.3 48.87,2.3 48.88,2.29 48.88))"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 35,
                "intersecting" : "POLYGON((2.29 48.88,2.29 48.87,2.3 48.87,2.3 48.88,2.29 48.88))"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_42" : {
        "id" : 42,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":42,
                        "level":" { country } "
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id":42,
                "level":" { country } "
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_43" : {
        "id" : 43,
        "layer_type" : "raster",
        "params" : """{
                        "data.ds_id":43
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 43               
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_45" : {
        "id" : 45,
        "layer_type" : "raster",
        "params" : """{"data.ds_id":45}""",
        "json_params" : {
            "parameters" : {
                "data.ds_id" : 45
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_46" : {
        "id" : 46,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":46,
                        "start_at":"''2018-01-01''",
                        "fields":{
                            "Pollutant":"Carbon dioxide"
                        }
                    }
                    """,
        "json_params" : {
            "parameters" : {
                "data.ds_id":46,
                "start_at":"'2018-01-01'",
                "fields":{
                    "Pollutant":"Carbon dioxide"
                }
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_47" : {
        "id" : 47,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":47,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id":47,
                "start_at":"'2018-01-01'"               
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_48" : {
        "id" : 48,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":48,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id":48,
                "start_at":"'2018-01-01'"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_49" : {
        "id" : 49,
        "layer_type" : "vector",
        "params" : """{
                        "data.ds_id":49,
                        "start_at":"''2018-01-01''"
                    }""",
        "json_params" : {
            "parameters" : {
                         "data.ds_id":49,
                        "start_at":"'2018-01-01'"               
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    },
    "DS_50" : {
        "id" : 50,
        "layer_type" : "vector",
        "params" : """{
                    "data.ds_id":50,
                    "start_at":"''2018-01-01''"
                }""",
        "json_params" : {
            "parameters" : {
                "data.ds_id":50,
                "start_at":"'2018-01-01'"
            },
            "row_limit" : 100000
        },
        "legend" : "blablabla"
    }
}