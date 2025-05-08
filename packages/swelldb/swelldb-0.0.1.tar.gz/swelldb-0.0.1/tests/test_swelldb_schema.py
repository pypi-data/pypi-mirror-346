# Copyright (c) 2025 Victor Giannakouris
# 
# This file is part of SwellDB and is licensed under the MIT License.
# See the LICENSE file in the project root for more information.

import unittest

from swelldb.table_plan.swelldb_attribute import SwellDBAttribute
from swelldb.table_plan.swelldb_schema import SwellDBSchema, SwellDBSchemaBuilder

import pyarrow as pa


class TestSwellDBUsage(unittest.TestCase):
    def test_schema_1(self):
        builder: SwellDBSchemaBuilder = SwellDBSchemaBuilder()

        schema: SwellDBSchema = (
            builder.add_attribute("name", pa.string(), description="just a name")
            .add_attribute("age", pa.int32(), description=None)
            .add_attribute("text_field", pa.string(), description=None)
        ).build()

        self.assertEquals(len(schema.get_attributes()), 3)

        self.assertEquals(schema.get_attribute("name").get_name(), "name")
        self.assertEquals(schema.get_attribute("age").get_name(), "age")
        self.assertEquals(schema.get_attribute("text_field").get_name(), "text_field")

        self.assertEquals(schema.get_attribute("name").get_data_type(), pa.string())
        self.assertEquals(schema.get_attribute("age").get_data_type(), pa.int32())
        self.assertEquals(
            schema.get_attribute("text_field").get_data_type(), pa.string()
        )
