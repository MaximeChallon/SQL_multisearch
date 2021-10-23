#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SQL_multisearch.SQL_multisearch
    Moteur de recherche multi-champs SQL.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :copyright: (c) 2021 by Maxime Challon.
    :license: MIT, see LICENSE for more details.
"""

from .log import *

def build_where(table: str, field: dict, request: dict, type_db:str):
    where = "select * from " + str(table) + " where " + str(field["field"])

    if "like" in request["operande"] or (type_db in ["sqlite"] and "ilike" in request["operande"]):
        if request["operande"] == "like":
            where = where + " like '%" + str(request["value"]) + "%'"
        elif "left" in request["operande"]:
            where = where + " like '%" + str(request["value"]) + "'"
        elif "right" in request["operande"]:
            where = where + " like '" + str(request["value"]) + "%'"
        else:
            where = where + " like '%" + str(request["value"]) + "%'"

    if type_db not in  ["sqlite"] and "ilike" in request["operande"]:
        if request["operande"] == "ilike":
            where = where + " ilike '%" + str(request["value"]) + "%'"
        elif "left" in request["operande"]:
            where = where + " ilike '%" + str(request["value"]) + "'"
        elif "right" in request["operande"]:
            where = where + " ilike '" + str(request["value"]) + "%'"
        else:
            where = where + " ilike '%" + str(request["value"]) + "%'"

    if request["operande"] == "=":
        if request["value_type"] == "int":
            where = where + " == " + str(request["value"]) + ""
        if request["value_type"] == "str":
            where = where + " == '" + str(request["value"]) + "'"

    return where


def tuple_to_json(result_tuple: tuple, fields: list, priority: int, searchable_fields:list, request:dict):
    out = { "values": {}}
    i = 0
    liste_searchable_fields = [field["field"] for field in searchable_fields]
    priority = priority

    for value in result_tuple:

        if "schema" in request:
            if fields[i] in request["schema"]:
                out["values"][fields[i]] = value
        else:
            out["values"][fields[i]] = value
        
        if fields[i] in liste_searchable_fields:
            if value:
                if request["value"] in value:
                    priority += len(request["value"])/len(value)
        i += 1
    out["ranking"] = priority
    return out


class Search:
    def __init__(
        self,
        db: object,
        table: str,
        request: dict,
        searchable_fields: list,
        fields_names: list,
        connexion_infos:dict,
    ):
        self.db = db
        self.table = table
        self.request = request
        self.searchable_fields = searchable_fields
        self.fields_names = fields_names
        self.return_objects = []
        self.type_db = connexion_infos["db_system"]

    def search(self):
        print_log("RUNNING", 200, "Research execution")
        for field in self.searchable_fields:
            results = self.db.execute(
                build_where(self.table, field, self.request, self.type_db)
            ).fetchall()
            for result in results:
                self.return_objects.append(
                    tuple_to_json(result, self.fields_names, int(field["priority"]), self.searchable_fields, self.request)
                )
        
        if "limit" in self.request:
            self.return_objects = sorted(self.return_objects, key=lambda d:d["ranking"], reverse=True)[:self.request["limit"]]
        print_log("OK", 200, "Research succeeded: "+ str(len(self.return_objects)) + " objects returned")
        return self.return_objects
    
    def get_columns_name(self):
        if self.type_db == "sqlite":
            result = [r[1] for r in self.db.execute("PRAGMA table_info("+self.table+")").fetchall()]
        else :
            result = None
        print_log("OK", 200, "Column names got: " + str(len(result)) + " fiels returned")
        return result