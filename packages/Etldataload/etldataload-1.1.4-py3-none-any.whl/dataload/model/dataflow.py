import pandas as pd
import dataload.model.datastorageconnection as con
from typing import Callable, Any, Dict, List

class DataFlow:
    def __init__(self, data):
        self.steps = []  # Liste des étapes de transformation
        self.data = data  # Stocke les données après extraction ou transformation

    def add_step(self, transformation: Callable, *args, **kwargs) -> 'DataFlow':
        self.steps.append((transformation, args, kwargs))
        return self

    def execute(self) -> 'DataFlow':
        for step, args, kwargs in self.steps:
           self.data = step(self.data, *args, **kwargs)
        return self

    def write_data(self, connect: con.DataStorageConnection, table, key_columns=None):
        if self.data is None:
            raise ValueError("No data to write. Run execute() first.")

        connect.write_data(df=self.data, table=table, key_columns=key_columns)
        return self.data

    def print(self):
        print(self.data.head())

    def __str__(self) -> str:
        """Représentation en chaîne pour le débogage."""
        return f"DataFlow(source={self.source.get('name')}, target={self.target.get('name')}, steps={len(self.steps)})"

