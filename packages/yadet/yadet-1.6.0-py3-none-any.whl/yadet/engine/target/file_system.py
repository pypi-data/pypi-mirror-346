from yadet.engine.target.base import TargetFileSystemEngine, TargetEngine
from yadet.helpers.json import meta_handler

import gzip
import json
import os
from pathlib import Path
from typing import Dict, List


class FileSystemTargetEngine(TargetEngine):

    def __init__(self, base_directory: str, compression: str = None):
        super().__init__(vendor=TargetFileSystemEngine)
        self.base_directory = base_directory
        self.compression = compression
        # TODO: Partitions

    def batch_directory(self, batch_key: str) -> os.PathLike:
        return os.path.join(self.base_directory, batch_key)

    def write_batch(self, table_name: str, data: List[Dict], batch_key: str, start_indx: int):
        table_directory = os.path.join(self.batch_directory(batch_key), table_name)
        Path(table_directory).mkdir(parents=True, exist_ok=True)

        if self.compression is None:
            with open(os.path.join(table_directory, f"{batch_key}-{start_indx}.json"), "w") as f:
                json.dump(data, f)
                
        elif self.compression == "gzip":
            with gzip.open(os.path.join(table_directory, f"{batch_key}-{start_indx}.json.gz"), "w") as f:
                f.write(json.dumps(data).encode('utf-8'))
        
        else:
            raise NotImplementedError(f"Compression=`{self.compression}` not available")


    def write_meta(self, meta: Dict, batch_key: str):
        Path(self.batch_directory(batch_key)).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(self.batch_directory(batch_key), "meta.json"), "w") as f:
            json.dump(meta, f, default=meta_handler, indent=4)