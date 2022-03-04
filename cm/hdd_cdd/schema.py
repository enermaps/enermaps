#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from pprint import pprint

from BaseCM import cm_hddcdd as hc

schema = hc.get_hddcdd_schema(save=True, schema_path=Path("schema.json"))
print("Generated schema:")
pprint(schema)
