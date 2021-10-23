#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SQL_multisearch.SQL_multisearch
    Moteur de recherche multi-champs SQL.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :copyright: (c) 2021 by Maxime Challon.
    :license: MIT, see LICENSE for more details.
"""

from .moduls.db import Connect
from .moduls.search import Search
from .moduls.log import *


class SQL_multisearch:
    def __init__(
        self,
        connexion_infos: dict,
        request: dict,
        searchable_fields: list,
        fields_names: list = [],
    ):
        self.connexion_infos = connexion_infos
        self.request = request
        self.searchable_fields = searchable_fields

        self.db = Connect(self.connexion_infos).sqlite()

        #tenter de nommer les champs de retour
        if len(fields_names) != 0:
            self.fields_names = fields_names
        elif self.connexion_infos["db_system"] == "sqlite":
            self.fields_names = [r[1] for r in self.db.execute("PRAGMA table_info("+self.connexion_infos["db_table"]+")").fetchall()]
        else:
            # créer liste au hasard de noms de champs aléatoires avec nombre de valeurs qu'a une entrée en table
            self.fields_names = [
                "field" + str(i)
                for i in range(
                    1,
                    len(
                        self.db.execute(
                            "select * from "
                            + str(self.connexion_infos["db_table"])
                            + " limit 1"
                        ).first()
                    )
                    + 1,
                )
            ]

    def _count(self):
        return len(self._results())

    def _results(self):
        return Search(
            self.db,
            self.connexion_infos["db_table"],
            self.request,
            self.searchable_fields,
            self.fields_names,
            self.connexion_infos,
        ).search()
    
    def _columns(self):
        return Search(
            self.db,
            self.connexion_infos["db_table"],
            self.request,
            self.searchable_fields,
            self.fields_names,
            self.connexion_infos,
        ).get_columns_name()
    
    def _stats(self):
        stats = {"ranks":{}}
        for r in self._results():
            if str(r["ranking"]) in stats["ranks"].keys():
                stats["ranks"][str(r["ranking"])] = int(stats["ranks"][str(r["ranking"])])+1
            else:
                stats["ranks"][str(r["ranking"])] = 1
            
            if "total" in stats:
                stats["total"] = int(stats["total"])+1
            else:
                stats["total"] = 1
        return stats