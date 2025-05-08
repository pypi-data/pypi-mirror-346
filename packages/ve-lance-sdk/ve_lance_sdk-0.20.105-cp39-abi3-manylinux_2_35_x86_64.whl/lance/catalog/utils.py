# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Lance Authors

import logging
from typing import Tuple, Union, Type

import pyarrow as pa
from las_rest.core.entity.table import FieldColumn

Identifier = Tuple[str, ...]
TableIdentifier = Union[str, Identifier]

class Utils:
    @staticmethod
    def identifier_to_database(
            identifier: TableIdentifier, err: Union[Type[ValueError], Type[Exception]] = ValueError
    ) -> str:
        tuple_identifier = Utils.identifier_to_tuple(identifier)
        if len(tuple_identifier) != 1:
            raise err(f"Invalid database, hierarchical namespaces are not supported: {identifier}")
        return tuple_identifier[0]


    @staticmethod
    def identifier_to_tuple(identifier: TableIdentifier) -> Identifier:
        """Parse an identifier to a tuple.

        If the identifier is a string, it is split into a tuple on '.'. If it is a tuple, it is used as-is.

        Args:
            identifier (str | Identifier): an identifier, either a string or tuple of strings.

        Returns:
            Identifier: a tuple of strings.
        """
        return identifier if isinstance(identifier, tuple) else tuple(str.split(identifier, "."))


    @staticmethod
    def identifier_to_database_and_table(identifier: TableIdentifier
    ) -> Tuple[str, str]:
        """
        Convert an identifier to a tuple containing the database name and table name.

        This method takes an identifier and raises ValueError if the identifier format is invalid.

        Args:
            identifier (TableIdentifier): The identifier to convert.

        Returns:
            Tuple[str, str]: A tuple containing the database name and table name.

        Raises:
            ValueError: If the identifier format is invalid
        """
        # Convert the identifier to a tuple
        tuple_identifier = Utils.identifier_to_tuple(identifier)
        # Check if the tuple has exactly two elements
        if len(tuple_identifier) != 2:
            # Raise an error if the tuple does not have exactly two elements
            raise ValueError(f"Invalid identifier format, expected [database].[table]: {identifier}")
        # Return the database name and table name as a tuple
        return tuple_identifier[0], tuple_identifier[1]

    @staticmethod
    def rename_scheme(location):
        if not location:  # 处理 None 或空字符串
            return location

        # 按优先级替换协议头
        for prefix in ["s3a://", "tos://"]:
            if location.startswith(prefix):
                return "s3://" + location[len(prefix):]

        return location


    @staticmethod
    def get_schema_from_source(data_obj: any) -> [FieldColumn]:
        match type(data_obj):
            case pa.Table:
                return Utils.arrow_table_to_field_columns(data_obj)
            case pa.RecordBatch:
                return Utils.arrow_table_to_field_columns(pa.Table.from_batches([data_obj]))
            case pa.RecordBatchReader:
                return Utils.arrow_table_to_field_columns(data_obj.read_all())
            case _:
                logging.info("schema cannot be inferred for this source type, current only supports pyarrow")
                return None

    @staticmethod
    def arrow_table_to_field_columns(table: pa.Table) -> [FieldColumn]:
        schema = table.schema
        field_columns = []
        for field in schema:
            column_name = field.name
            # 使用 arrow_to_hive_type 函数获取 Hive 型
            arrow_type_instance = field.type
            hive_type = Utils.arrow_to_hive_type(arrow_type_instance)
            column_type = hive_type

            column_desc = None
            if field.metadata and b'description' in field.metadata:
                column_desc = field.metadata[b'description'].decode('utf-8')

            field_columns.append(FieldColumn(column_name=column_name, column_type=column_type, column_desc=column_desc))

        return field_columns

    @staticmethod
    def arrow_to_hive_type(arrow_type):
        # 基础类型映射（移除了decimal的固定映射）
        type_mapping = {
            pa.int8(): 'tinyint',
            pa.int16(): 'smallint',
            pa.int32(): 'int',
            pa.int64(): 'bigint',
            pa.float32(): 'float',
            pa.float64(): 'double',
            pa.bool_(): 'boolean',
            pa.string(): 'string',
            pa.binary(): 'binary',
            pa.date32(): 'date',
            pa.timestamp('ms'): 'timestamp'
        }

        # process decimal
        if isinstance(arrow_type, (pa.Decimal128Type, pa.Decimal256Type)):
            precision = arrow_type.precision
            scale = arrow_type.scale
            return f"decimal({precision},{scale})"

        if pa.types.is_timestamp(arrow_type):
            return 'timestamp'

        if pa.types.is_list(arrow_type):
            element_type = Utils.arrow_to_hive_type(arrow_type.value_type)
            return f"array<{element_type}>"

        # default as string
        return type_mapping.get(arrow_type, 'string')
