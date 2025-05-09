
# Raga Testing Platform

The `raga-testing-platform` package provides a Python client for interacting with the Raga Testing Platform. It allows you to easily create and manage test sessions, datasets, and perform various testing operations.


## Installation
You can install `raga-testing-platform` using pip:

`pip install raga-testing-platform`

## Usage
To use the package, import the necessary classes and modules:

```
from raga import Dataset, TestSession, Auth
import pandas as pd
from typing import Optional, List, Dict
```
### Creating a test DataFrame

```
test_df = pd.DataFrame({
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c']
})
```
### Defining the Schema class

```
class Schema:
    def __init__(
        self,
        prediction_id: Optional[str] = None,
        timestamp_column_name: Optional[str] = None,
        feature_column_names: Optional[List[str]] = None,
        metadata_column_names: Optional[List[str]] = None,
        label_column_names: Optional[Dict[str, str]] = None,
        embedding_column_names: Optional[Dict[str, str]] = None,
    ):
        self.prediction_id = prediction_id
        self.timestamp_column_name = timestamp_column_name
        self.feature_column_names = feature_column_names
        self.metadata_column_names = metadata_column_names
        self.label_column_names = label_column_names
        self.embedding_column_names = embedding_column_names
```

### Creating an instance of the Schema class
```
schema = Schema()
```

### Creating an instance of the Auth class
It will create auth token for further usages.
```
auth = Auth()
```

This variable stores auth token. You can use it untill expire token.
```
auth.token
```

### Creating an instance of the TestSession class
In this instance `experiment` will create and return `experiment_id`
```
experiment_id = TestSession(token, 1, "my_experiment")
```
This variable stores `experiment_id`. You can use it in further experiment.
```
experiment_id.experiment_id
```
### Creating an instance of the Dataset class

```
test_ds = Dataset(token, experiment_id, test_df, schema, "DatasetName")
```

### Loading labels from a file

```
test_ds.load_labels_from_file(
    "/path/to/labels.json",
    "dataset_name",
    "id_column_name",
    "label_column_name",
    "metadata_column_name",
    "category_column_name",
    "category_id_column_name"
)
```

### To Debug
```
export DEBUG=1
```