#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SQL_multisearch.SQL_multisearch
    Moteur de recherche multi-champs SQL.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :copyright: (c) 2021 by Maxime Challon.
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

def print_log(status:str,code_status:int, message:str):
    print(str(datetime.today()) + " | " + status + " | " + str(code_status) + " | " + message)