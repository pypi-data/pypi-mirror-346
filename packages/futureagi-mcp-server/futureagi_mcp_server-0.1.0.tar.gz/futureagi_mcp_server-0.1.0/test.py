
# pip install futureagi

import os
os.environ["FI_API_KEY"] = "1f440a439af4457e90f870ab94671853"
os.environ["FI_SECRET_KEY"] = "1e202979b9804b958160370ab09f18f1"
os.environ["FI_BASE_URL"] = "https://api.futureagi.com"

from fi.datasets import DatasetClient

columns = [
    {
        "name": "text",
        "data_type": "text"
    },
    {
        "name": "label",
        "data_type": "integer"
    }
]

rows = [
    {
        "cells": [
            {
                "column_name": "text",
                "value": "Hello, world!"
            },
            {
                "column_name": "label",
                "value": 0
            }
        ]
    }
]

try:
    DatasetClient.add_dataset_columns(dataset_name="New Dataset", columns=columns)
    DatasetClient.add_dataset_rows(dataset_name="New Dataset", rows=rows)

except Exception as e:
    print(f"Failed to add data: {e}")
