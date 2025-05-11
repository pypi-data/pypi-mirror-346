# YADET (Yet Another Data Extract Tool)

A simple and effective Python data extraction tool for getting batch data exports 
and store in a simple format.  

Current functionality is relatively limited with MsSQL Source integration
and File System Target Integration.

## Install 

With Python 3.7 or greater install the package with simple pip command.

```
pip install yadet
```

## Usage


Import and load data
```python
from yadet.config import ProjectConfig
from yadet.batch import ProjectBatchRun
from yadet.engine import SourceMssqlEngine, TargetFileSystemEngine

import os

conn_str = "<>"

project = ProjectConfig(
    name="example", 
    source_engine=SourceMssqlEngine, 
    source_engine_params={"connection_str": conn_str}, 
    target_engine=TargetFileSystemEngine, 
    target_engine_params={
        "base_directory": os.path.join("data", "example"), "compression": "gzip"
    }
)

batch_run = ProjectBatchRun(project=project, debug=True)
batch_run.run_batch()
```