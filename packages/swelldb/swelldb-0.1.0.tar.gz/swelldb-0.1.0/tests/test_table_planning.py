# Copyright (c) 2025 Victor Giannakouris
# 
# This file is part of SwellDB and is licensed under the MIT License.
# See the LICENSE file in the project root for more information.
import json

import pytest
from unittest.mock import Mock, patch
import pyarrow as pa

from swelldb.engine.datafusion_processor import DataFusionEngine
from swelldb.table_plan.planner import TableGenPlanner
from swelldb.table_plan.table.logical.logical_table import LogicalTable
from swelldb.table_plan.swelldb_schema import SwellDBSchema


@pytest.fixture
def mock_llm():
    return Mock()


@pytest.fixture
def mock_logical_table():
    schema = SwellDBSchema.from_string("name str, age int")
    return LogicalTable(name="test_table", prompt="test content", schema=schema)


@pytest.fixture
def planner(mock_llm):
    return TableGenPlanner(llm=mock_llm, execution_engine=DataFusionEngine(), serper_api_key=None)


def test_planner_initialization(mock_llm):
    planner = TableGenPlanner(llm=mock_llm, execution_engine=DataFusionEngine(), serper_api_key=None)
    assert planner._llm == mock_llm


def test_create_plan(planner, mock_logical_table, mock_llm):
    # Arrange
    base_columns = ["name"]
    mock_llm.call.return_value = json.dumps(
        {
            "columns": [],
            "query": None
        }
    )

    # Act
    plan = planner.create_plan(
        logical_table=mock_logical_table, base_columns=base_columns
    )

    # Assert
    assert plan is not None
    mock_llm.call.assert_called_once()


def test_create_plan_with_invalid_response(planner, mock_logical_table, mock_llm):
    # Arrange
    base_column = "name"
    mock_llm.call.return_value = "invalid_json"

    # Act & Assert
    with pytest.raises(ValueError):
        planner.create_plan(logical_table=mock_logical_table, base_column=base_column)


def test_create_plan_with_missing_base_column(planner, mock_logical_table):
    # Act & Assert
    with pytest.raises(ValueError, match="Base column must be specified"):
        planner.create_plan(logical_table=mock_logical_table, base_column=None)


@patch("swelldb.table_plan.planner.TableGenPlanner._validate_plan")
def test_create_plan_with_validation(
    mock_validate, planner, mock_logical_table, mock_llm
):
    # Arrange
    base_column = "name"
    mock_llm.call.return_value = '{"plan": "test_plan"}'
    mock_validate.return_value = True

    # Act
    plan = planner.create_plan(
        logical_table=mock_logical_table, base_column=base_column
    )

    # Assert
    assert plan is not None
    mock_validate.assert_called_once()


def test_create_plan_with_complex_schema(planner, mock_llm):
    # Arrange
    schema = SwellDBSchema.from_string(
        """
        name str,
        age int,
        address {
            street str,
            city str,
            zip str
        }
    """
    )
    logical_table = LogicalTable(
        name="test_table", prompt="test content", schema=schema
    )
    base_column = "name"
    mock_llm.call.return_value = '{"plan": "test_plan"}'

    # Act
    plan = planner.create_plan(logical_table=logical_table, base_column=base_column)

    # Assert
    assert plan is not None
    mock_llm.call.assert_called_once()


def test_create_plan_with_data(planner, mock_logical_table, mock_llm):
    # Arrange
    base_column = "name"
    data = pa.table({"name": ["John", "Jane"], "age": [30, 25]})
    mock_llm.call.return_value = '{"plan": "test_plan"}'

    # Act
    plan = planner.create_plan(
        logical_table=mock_logical_table, base_column=base_column, data=data
    )

    # Assert
    assert plan is not None
    mock_llm.call.assert_called_once()
