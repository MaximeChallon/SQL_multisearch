#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SQL_multisearch.SQL_multisearch
    Moteur de recherche multi-champs SQL.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :copyright: (c) 2021 by Maxime Challon.
    :license: MIT, see LICENSE for more details.
"""

from sqlalchemy import create_engine
from .log import *

class Connect():
    def __init__(self, connexion_infos):
        self.connexion_infos = connexion_infos
        print_log("RUNNING", 200,  self.connexion_infos["db_system"] + " connexion initating on " + self.connexion_infos["db_url"])

    # créer une fonction par type de db (mysql, sqlite, postgre, maria, etc)
    def sqlite(self):
        engine = create_engine(self.connexion_infos["db_system"] + ':///' + self.connexion_infos["db_url"], echo = True)
        print_log("OK", 200,  self.connexion_infos["db_system"] + " connexion open")
        return engine
