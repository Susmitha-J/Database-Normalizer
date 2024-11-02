
import pandas as pd
import numpy as np
from tabulate import tabulate

# Relation class
class Relation:
    def __init__(self, headers, data, primary_key):
        """
        Relation Class  with attributes name headers data primary key foreign key dependencies
        """
        self.name = ""
        self.headers = headers
        self.data = data
        self.primary_key = primary_key
        self.foreign_key = []
        self.dependencies = []
    def add_name(self,name):
        self.name = name

    def add_foreign_key(self, foreign_key):
        #Adding Foreign keys to the relation if identified (Not working as expected)
        self.foreign_key.append(foreign_key)

    def add_dependency(self, dependency):
        #Adds a Dependency instance to the relation.
        self.dependencies.append(dependency)

    def build_schema(self):
        #Generating the SQL CREATE TABLE for the relation
        if not self.name:
            raise ValueError("Relation name is not present use add method to add name")

        # Creating the SQL statement
        schema = f"CREATE TABLE {self.name} (\n"
        column_defs = []

        for header in self.headers:
            column_defs.append(f"    {header} VARCHAR(255)")

        primary_key_str = f"    PRIMARY KEY ({', '.join(self.primary_key)})"
        column_defs.append(primary_key_str)

        for column, ref_table, ref_column in self.foreign_key:
            fk_str = f"    FOREIGN KEY ({column}) REFERENCES {ref_table}({ref_column})"
            column_defs.append(fk_str)

        schema += ",\n".join(column_defs)
        schema += "\n);"

        return schema

    def display(self):
        #This method prints the relation data in table form along with primary keys and functional dependencies
        print(self.name)
        print(tabulate(self.data, headers=self.headers, tablefmt='pretty'))
        print("Primary Key:", self.primary_key)
        print("Functional Dependencies:")
        for dep in self.dependencies:
            dep_type = "FD" if dep.dependency_type == "FD" else "MVD"
            print(f"  LHS: {dep.lhs} -> RHS: {dep.rhs} (Type: {dep_type})")
