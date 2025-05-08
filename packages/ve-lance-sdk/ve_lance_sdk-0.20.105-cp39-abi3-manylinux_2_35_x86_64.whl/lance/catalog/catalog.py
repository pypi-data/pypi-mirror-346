# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright The Lance Authors

import abc
from typing import Dict, List, Any
from .utils import TableIdentifier


class Catalog(abc.ABC):
    @abc.abstractmethod
    def create_database(self, database: str, location: str) -> Any:
        pass
        """Create a database namespace"""

    @abc.abstractmethod
    def drop_database(self, database: str) -> None:
        pass

    @abc.abstractmethod
    def convert_table_to_dataset_uri(self, identifier: TableIdentifier) -> str:
        pass

    @abc.abstractmethod
    def register_lance_table(
        self,
        identifier: TableIdentifier,
        schema: Any
    ):
        pass
        """Create a data table"""

    @abc.abstractmethod
    def list_tables(self, database: str) -> List[str]:
        """List all tables in the specified database"""

    @abc.abstractmethod
    def get_table(self, identifier: TableIdentifier):
        """Check if the table exists"""

    @abc.abstractmethod
    def table_exists(self, identifier: TableIdentifier) -> bool:
        """Check if the table exists"""

    @abc.abstractmethod
    def drop_table(self, identifier: TableIdentifier):
        """drop the table"""

    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: Dict[str, Any]) -> 'Catalog':
        pass


class CatalogFactory:
    @staticmethod
    def create(config: Dict[str, Any]) -> 'Catalog':
        """
        Dynamically create corresponding Catalog instance based on config features
        Priority logic:
        1. access_key exists -> LasCatalog
        2. hive.metastore.uris exists -> HiveCatalog
        3. Throw exception for unrecognized config types
        """
        catalog_type = CatalogFactory.get_catalog_type(config)

        if catalog_type == 'hive':
            from .hive_catalog import HiveCatalog
            return HiveCatalog.from_config(config)
        elif catalog_type == 'las':
            from .las_catalog import LasCatalog
            return LasCatalog.from_config(config)
        else:
            raise ValueError(f"Unsupported catalog type: {catalog_type}")

    @staticmethod
    def get_catalog_type(config: Dict[str, Any]) -> str:
        """
        Type detection logic (extensible):
        - Check for hive feature keys
        - Check for las feature keys
        """
        if 'hive.metastore.uris' in config:
            return 'hive'
        else:
            return 'las'