#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
from collections import OrderedDict as odict
from pathlib import Path
from typing import Any, Dict

from BaseCM import cm_hddcdd as hc

import refurbish as rf


def get_refurbish_schema(
    save: bool = False, schema_path: Path = None
) -> Dict[str, Any]:
    """Return a dictionary with the schema for the refurbish CM"""
    # get the schema for the HDDs and CDDs CM
    schema = hc.get_hddcdd_schema(save=False)
    props = schema["properties"]

    # extend the properties to the refurbish parameters
    yrs = hc.get_years()
    ref_yr = odict(
        type="integer",
        title="Reference year",
        description="",
        default=2050,
        minimum=min(yrs),
        maximum=max(yrs),
        enum=yrs,
    )
    props["reference year"] = ref_yr

    bstypes = sorted([bt for bt, tab in rf.BS2TABULA.items() if len(tab)])
    btype = odict(
        type="string",
        title="building typology",
        description="Building typology class",
        default=bstypes[0],
        enum=bstypes,
    )
    props["building typology"] = btype

    start_yr = odict(
        type="integer",
        title="start epoch of construction",
        description=(
            "Start epoch of construction year for the building to be refurbished"
        ),
        default=1960,
    )
    props["start epoch of construction"] = start_yr

    end_yr = odict(
        type="integer",
        title="end epoch of construction",
        description="End epoch of construction year for the building to be refurbished",
        default=1969,
    )
    props["end epoch of construction"] = end_yr

    basic_ref_rate = odict(
        type="number",
        title="Percentage of basic refurbished buildings",
        description=(
            "The percentage of building that has received a basic refurbish "
            "by the selected reference reference year"
        ),
        default=10.0,
        minimum=0,
        maximum=100.0,
    )
    props["percentage basic refurbish rate"] = basic_ref_rate

    advance_ref_rate = odict(
        type="number",
        title="Percentage of advance refurbished buildings",
        description=(
            "The percentage of building that has received an advance refurbish "
            "by the selected reference reference year"
        ),
        default=5.0,
        minimum=0,
        maximum=100.0,
    )
    props["percentage advance refurbish rate"] = advance_ref_rate

    if save is True:
        if schema_path is None:
            cmpath = hc.CURRENT_FILE_DIR.parent.parent.resolve()
            schema_path = cmpath / "refurbish" / "schema.json"

        with open(schema_path.as_posix(), mode="w") as schfile:
            json.dump(schema, schfile, indent=2)
    return schema


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Generate schema.json based on the data available on the repository."
        )
    )
    parser.add_argument(
        "--print-only",
        default=False,
        help=(
            "Print the result on stdout without saving the result "
            "to the 'schema.json' file"
        ),
        action="store_true",
    )
    args = parser.parse_args()
    schema = get_refurbish_schema(
        save=False if args.print_only else True, schema_path=Path("schema.json")
    )
    print("---------------------------------------------\nGenerated schema:")
    print(json.dumps(schema, indent=2))
