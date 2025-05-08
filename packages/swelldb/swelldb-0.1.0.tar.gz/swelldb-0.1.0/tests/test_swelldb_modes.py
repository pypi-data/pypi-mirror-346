# Copyright (c) 2025 Victor Giannakouris
# 
# This file is part of SwellDB and is licensed under the MIT License.
# See the LICENSE file in the project root for more information.

import os
import unittest

from swelldb import SwellDB
from swelldb.llm.openai_llm import OpenAILLM
from swelldb.table_plan.swelldb_schema import SwellDBSchema, SwellDBSchemaBuilder

import pyarrow as pa

import logging

from swelldb.swelldb import Mode, TableBuilder
from swelldb.table_plan.table.physical.dataset_table import DatasetTable
from swelldb.table_plan.table.physical.llm_table import LLMTable
from swelldb.table_plan.table.physical.physical_table import PhysicalTable
from swelldb.table_plan.table.physical.search_engine_table import SearchEngineTable

# Add info level logging
logging.basicConfig(level=logging.INFO)


class TestSwellDBPlanner(unittest.TestCase):
    def test_e2e_1(self):
        builder: SwellDBSchemaBuilder = SwellDBSchemaBuilder()

        schema: SwellDBSchema = (
            builder.add_attribute(
                "name", pa.string(), description="the state name"
            )
        ).build()

        swelldb: SwellDB = SwellDB(OpenAILLM())

        table_builder: TableBuilder = swelldb.table_builder()

        tbl: PhysicalTable = (
            table_builder.set_table_name("country")
            .set_content("a table of 5 US sates")
            .set_schema(schema)
            .set_base_columns(["name"])
            .set_table_gen_mode(Mode.OPERATORS)
            .set_operators([SearchEngineTable])
        ).build()

        print(tbl.materialize().to_pandas())

    def test_e2e_2(self):
        builder: SwellDBSchemaBuilder = SwellDBSchemaBuilder()

        schema: SwellDBSchema = (
            builder.add_attribute(
                "name", pa.string(), description="the state name"
            ).add_attribute(
                "governor_1995",
                pa.string(),
                description="the governor of that state in year 1995",
            )
        ).build()

        swelldb: SwellDB = SwellDB(OpenAILLM())

        table_builder: TableBuilder = swelldb.table_builder()

        tbl: PhysicalTable = (
            table_builder.set_table_name("country")
            .set_content("a table of 5 US sates")
            .set_schema(schema)
            .set_base_columns(["name"])
            .set_table_gen_mode(Mode.OPERATORS)
            .set_operators([SearchEngineTable])
        ).build()

        print(tbl.materialize().to_pandas())

    def test_e2e_3(self):
        swelldb: SwellDB = SwellDB(OpenAILLM())

        table_builder: TableBuilder = swelldb.table_builder()
        tbl: PhysicalTable = (
            table_builder.set_table_name("country")
            .set_content("a table of 5  US states")
            .set_schema("name str, population int")
            .set_base_columns(["name"])
            .set_table_gen_mode(Mode.OPERATORS)
            .set_operators([SearchEngineTable])
        ).build()

        print(tbl.materialize().to_pandas())

    def test_e2e_4(self):
        swelldb: SwellDB = SwellDB(OpenAILLM(temperature=0))

        # Create a dataframe with some states
        data: pa.Table = pa.Table.from_pydict(
            {"name": ["New York", "Illinois"], "state": ["NY", "IL"]}
        )

        table_builder: TableBuilder = swelldb.table_builder()
        tbl: PhysicalTable = (
            table_builder.set_table_name("country")
            .set_content("a table of US states")
            .set_schema("name str, state_population_1990 int, governor_1990 str")
            .set_base_columns(["name"])
            .set_data(data)
        ).build()

        tbl.explain()

        print(tbl.materialize().to_pandas())

    def test_e2e_builder(self):
        swelldb: SwellDB = SwellDB(OpenAILLM(temperature=0))
        table_builder: TableBuilder = swelldb.table_builder()

        file_dir = os.path.dirname(os.path.abspath(__file__))

        tbl: PhysicalTable = (
            table_builder.set_table_name("country")
            .set_content("a table of mutations")
            .set_schema("mut_name str, mutation_explanation str, web_link str")
            .set_table_gen_mode(Mode.OPERATORS)
            .set_operators([DatasetTable, LLMTable, SearchEngineTable])
            .set_base_columns(["mut_name"])
            .add_csv_file("mutations", os.path.join(file_dir, "test_files", "mutations.csv"))
            .add_csv_file("protein", os.path.join(file_dir, "test_files", "mutation_affected_protein.csv"))
        ).build()

        tbl.explain()

        print(tbl.materialize().to_pandas())

    def test_e2e_multi_key(self):
        swelldb: SwellDB = SwellDB(OpenAILLM(temperature=0))
        table_builder: TableBuilder = swelldb.table_builder()

        data: pa.Table = pa.Table.from_pydict(
            {
                "body_group": ["Upper", "Upper", "Lower"],
                "body_subgroup": ["Chest", "Back", "Legs"],
            }
        )

        tbl: PhysicalTable = (
            table_builder.set_table_name("exercises")
            .set_content("a table of exercises")
            .set_schema("body_group str, body_subgroup str, exercise_name str")
            .set_table_gen_mode(Mode.OPERATORS)
            .set_operators([LLMTable, SearchEngineTable])
            .set_base_columns(["body_group", "body_subgroup"])
            .set_data(data)
        ).build()

        tbl.explain()

        print(tbl.materialize().to_pandas())
