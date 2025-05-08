# Copyright (c) 2025 Victor Giannakouris
# 
# This file is part of SwellDB and is licensed under the MIT License.
# See the LICENSE file in the project root for more information.

import pytest
from unittest.mock import Mock, patch
import pyarrow as pa
from swelldb import SwellDB
from swelldb.llm.openai_llm import OpenAILLM
from swelldb.swelldb import Mode
from swelldb.table_plan.layout import Layout
from swelldb.table_plan.swelldb_schema import SwellDBSchema
from swelldb.engine.datafusion_processor import DataFusionEngine


@pytest.fixture
def mock_llm():
    return Mock(spec=OpenAILLM)


@pytest.fixture
def mock_execution_engine():
    return Mock(spec=DataFusionEngine)


@pytest.fixture
def swelldb(mock_llm, mock_execution_engine):
    return SwellDB(
        llm=mock_llm,
        execution_engine=mock_execution_engine,
        serper_api_key="test_key"
    )


def test_swelldb_initialization(mock_llm, mock_execution_engine):
    db = SwellDB(
        llm=mock_llm,
        execution_engine=mock_execution_engine,
        serper_api_key="test_key"
    )
    assert db._llm == mock_llm
    assert db._execution_engine == mock_execution_engine
    assert db._serper_api_key == "test_key"


def test_create_table_llm_mode(swelldb, mock_llm):
    # Arrange
    name = "test_table"
    content = "test content"
    schema = SwellDBSchema.from_string("name str, age int")
    layout = Layout.ROW()

    # Act
    table = swelldb._create_table(
        name=name,
        content=content,
        schema=schema,
        mode=Mode.LLM,
        layout=layout,
        chunk_size=20
    )

    # Assert
    assert table is not None
    mock_llm.call.assert_called()


def test_create_table_search_mode(swelldb, mock_llm):
    # Arrange
    name = "test_table"
    content = "test content"
    schema = SwellDBSchema.from_string("name str, age int")
    layout = Layout.ROW()

    # Act
    table = swelldb._create_table(
        name=name,
        content=content,
        schema=schema,
        mode=Mode.SEARCH,
        layout=layout,
        chunk_size=20
    )

    # Assert
    assert table is not None
    mock_llm.call.assert_called()


def test_create_table_planner_mode(swelldb, mock_llm):
    # Arrange
    name = "test_table"
    content = "test content"
    schema = SwellDBSchema.from_string("name str, age int")
    layout = Layout.ROW()
    base_columns = ["name"]

    # Act
    table = swelldb._create_table(
        name=name,
        content=content,
        schema=schema,
        mode=Mode.PLANNER,
        layout=layout,
        base_columns=base_columns,
        chunk_size=20
    )

    # Assert
    assert table is not None
    mock_llm.call.assert_called()


def test_create_table_invalid_mode(swelldb):
    # Arrange
    name = "test_table"
    content = "test content"
    schema = SwellDBSchema.from_string("name str, age int")
    layout = Layout.ROW()

    # Act & Assert
    with pytest.raises(ValueError, match="Unknown mode"):
        swelldb._create_table(
            name=name,
            content=content,
            schema=schema,
            mode="INVALID",
            layout=layout,
            chunk_size=20
        )


def test_create_table_with_data(swelldb, mock_llm):
    # Arrange
    name = "test_table"
    content = "test content"
    schema = SwellDBSchema.from_string("name str, age int")
    layout = Layout.ROW()
    data = pa.table({"name": ["John", "Jane"], "age": [30, 25]})

    # Act
    table = swelldb._create_table(
        name=name,
        content=content,
        schema=schema,
        mode=Mode.LLM,
        layout=layout,
        data=data,
        chunk_size=20
    )

    # Assert
    assert table is not None
    mock_llm.call.assert_called()


def test_create_table_planner_mode_missing_base_columns(swelldb):
    # Arrange
    name = "test_table"
    content = "test content"
    schema = SwellDBSchema.from_string("name str, age int")
    layout = Layout.ROW()

    # Act & Assert
    with pytest.raises(ValueError, match="Base columns must be specified in planner mode"):
        swelldb._create_table(
            name=name,
            content=content,
            schema=schema,
            mode=Mode.PLANNER,
            layout=layout,
            chunk_size=20
        )


@patch("swelldb.table_plan.planner.TableGenPlanner")
def test_planner_initialization(mock_planner, mock_llm, mock_execution_engine):
    # Arrange
    db = SwellDB(
        llm=mock_llm,
        execution_engine=mock_execution_engine,
        serper_api_key="test_key"
    )

    # Assert
    mock_planner.assert_called_once_with(
        llm=mock_llm,
        execution_engine=mock_execution_engine,
        serper_api_key="test_key"
    )
