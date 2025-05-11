from yadet.config.table import TableConfig
from yadet.engine.source.base import SourceMssqlEngine
from yadet.engine.source.mssql import MsSqlSourceEngine
from yadet.engine.target.base import TargetFileSystemEngine
from yadet.engine.target.file_system import FileSystemTargetEngine
from yadet.helpers.json import meta_handler
from yadet.objects.base import BaseObject

import json
import os
from pathlib import Path
from typing import Dict, List, Union


class ProjectConfig(BaseObject):

    def __init__(self, 
                 name: str,
                 source_engine: str = SourceMssqlEngine,
                 source_engine_params: Dict = {},
                 target_engine: str = TargetFileSystemEngine,
                 target_engine_params: Dict = {},
                 config_dir: Union[str, os.PathLike] = "config") -> None:
        self.name = name
        self.source_engine: str = source_engine
        self.source_engine_params: Dict = source_engine_params
        self.target_engine: str = target_engine
        self.target_engine_params: Dict = target_engine_params
        self.config_dir: Union[str, os.PathLike] = config_dir

        self._tables_config: List[TableConfig] = []
        self._project_table_index: Dict[str, Dict] = {}
        
        self.open()

    @property
    def project_directory(self) -> os.PathLike:
        return os.path.join(self.config_dir, self.name)
        
    @property
    def table_config_filename(self) -> os.PathLike:
        return os.path.join(self.project_directory, "project_config.json")

    @property
    def table_index_filename(self) -> os.PathLike:
        return os.path.join(
            self.target_engine_params["base_directory"], "project_table_index.json"
        )

    @property
    def tables_config(self) -> List[TableConfig]:
        return sorted(self._tables_config, key= lambda x: x.ordinal)

    @property
    def project_table_index(self) -> Dict[str, Dict]:
        return self._project_table_index

    @property
    def base_config(self) -> Dict:
        return {
            "name": self.name,
            "source_engine": self.source_engine,
            "target_engine": self.target_engine
        }
    
    def open(self):
        # Open Project Config
        if os.path.exists(self.table_config_filename):
            with open(self.table_config_filename, "r") as f:
                project_config = json.load(f)
                for config in project_config["items"]:
                    self.add_table_config(TableConfig(**config))
                # TODO: Add Engine
        else:
            Path(self.project_directory).mkdir(parents=True, exist_ok=True)
            with open(self.table_config_filename, "w") as f: 
                json.dump({**self.base_config, "items": []}, f)

        # Open Project Table Index
        if os.path.exists(self.table_index_filename):
            with open(self.table_index_filename, "r") as f:
                self._project_table_index = json.load(f)
        else:
            # Ensure Directory exists
            Path(
                os.path.dirname(self.table_index_filename)
            ).mkdir(parents=True, exist_ok=True)

            # Save Base Project Table Index
            with open(self.table_index_filename, "w") as f: 
                json.dump({}, f)

    def get_source_engine(self):
        if self.source_engine == SourceMssqlEngine:
            return MsSqlSourceEngine(**self.source_engine_params)
        raise NotImplementedError(f"Engine Type {self.source_engine} not active")
    
    def get_target_engine(self):
        if self.target_engine == TargetFileSystemEngine:
            return FileSystemTargetEngine(**self.target_engine_params)
        raise NotImplementedError(f"Engine Type {self.target_engine} not active")
        
    def save(self):
        Path(self.project_directory).mkdir(parents=True, exist_ok=True)
        with open(self.table_config_filename, "w") as f: 
            json.dump({
                **self.base_config, 
                "items": [table.data for table in self.tables_config]
            }, f, indent=4)

        with open(self.table_index_filename, "w") as f:
            json.dump(self.project_table_index, f, default=meta_handler, indent=4)
            
    def add_table_config(self, table_config: TableConfig):
        self._tables_config.append(table_config)

    def __str__(self) -> str:
        return str(self.name)