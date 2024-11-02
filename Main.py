
import pandas as pd
import numpy as np 
from Normalization import (
    is_1nf, normalize_1nf_relation, check_all_relations_2nf, decompose_to_2nf,
    check_all_relations_3nf, decompose_to_3nf, check_all_relations_bcnf,
    decompose_to_bcnf, check_all_relations_4nf, decompose_to_4nf, 
    check_all_relations_5nf, decompose_to_5nf, decompose_to_5nf_relation_ip
)
from Relation import Relation
from Input import read_dependencies_from_file, validate_and_add_dependencies

import pandas as pd
import numpy as np

def ensure_dict_format(relations):
    """
    Ensure that relations are in dictionary format.
    If a single Relation instance is provided, convert it to a dictionary.
    
    Parameters:
        relations (Relation or dict): Relation instance or dictionary of Relation instances.
    
    Returns:
        dict: Dictionary of relations.
    """
    if isinstance(relations, Relation):
        return {relations.name: relations}
    return relations

def main():
    # Read Excel file
    file_path = input("Enter the filename for the relation (e.g., 'relationinput.xlsx'): ")
    df = pd.read_excel(file_path)

    fd_filename = input("Enter the filename for functional dependencies (e.g., 'FD.txt'): ")

    # Extract headers and data
    headers = list(df.columns)
    data = df.values.tolist()

    # Get primary key input from the user
    primary_key = input("Enter the primary keys, separated by commas: ").split(',')
    primary_key = [key.strip() for key in primary_key]

    # Create Relation instance
    relation = Relation(headers, data, primary_key)
    relation.add_name("InputRelation")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("\nInput Relation:")
    relation.display()
    print("--------------------------------------------------------------------------------------------------------------------")

    # Ask the user to select the highest form of normalization
    print("Select the highest level of normalization you want to achieve:")
    print("1. 1NF")
    print("2. 2NF")
    print("3. 3NF")
    print("4. BCNF")
    print("5. 4NF")
    print("6. 5NF")
    choice = int(input("Enter your choice (1-6): "))

    # Check 1NF and normalize if needed
    is_in_1nf, non_1nf_attributes = is_1nf(relation)
    if is_in_1nf:
        print("RELATION IS ALREADY IN 1NF")
        dependencies = read_dependencies_from_file(fd_filename)
        relations = validate_and_add_dependencies(ensure_dict_format(relation), dependencies)
    else:
        normalized_relations_dict = normalize_1nf_relation(relation, non_1nf_attributes)
        dependencies = read_dependencies_from_file(fd_filename)
        relations = validate_and_add_dependencies(normalized_relations_dict, dependencies)
        print("AFTER 1NF NORMALIZATION")
        for rel in normalized_relations_dict.values():
            rel.display()
            print(rel.build_schema())
        print("-----------------------------------------------------------------------------------------------------------------")

    if choice == 1:
        return

    # Decompose to 2NF
    print("2NF")
    if check_all_relations_2nf(ensure_dict_format(relations)):
        print("RELATIONS ARE ALREADY IN 2NF")
        relations_2nf = relations
    else:
        relations_2nf = decompose_to_2nf(ensure_dict_format(relations))
        print("AFTER 2NF NORMALIZATION")
        for rel in relations_2nf.values():
            rel.display()
            print(rel.build_schema())
        print("-----------------------------------------------------------------------------------------------------------------")

    if choice == 2:
        return

    # Decompose to 3NF
    print("3NF")
    if check_all_relations_3nf(ensure_dict_format(relations_2nf)):
        print("RELATIONS ARE ALREADY IN 3NF")
        relations_3nf = relations_2nf
    else:
        relations_3nf = decompose_to_3nf(ensure_dict_format(relations_2nf))
        print("AFTER 3NF NORMALIZATION")
        for rel in relations_3nf.values():
            rel.display()
            print(rel.build_schema())
        print("-----------------------------------------------------------------------------------------------------------------")

    if choice == 3:
        return

    # Decompose to BCNF
    print("BCNF")
    if check_all_relations_bcnf(ensure_dict_format(relations_3nf)):
        print("RELATIONS ARE ALREADY IN BCNF")
        relations_bcnf = relations_3nf
    else:
        relations_bcnf = decompose_to_bcnf(ensure_dict_format(relations_3nf))
        print("AFTER BCNF NORMALIZATION")
        for rel in relations_bcnf.values():
            rel.display()
            print(rel.build_schema())
        print("-----------------------------------------------------------------------------------------------------------------")

    if choice == 4:
        return

    # Decompose to 4NF
    print("4NF")
    if check_all_relations_4nf(ensure_dict_format(relations_bcnf)):
        print("RELATIONS ARE ALREADY IN 4NF")
        relations_4nf = relations_bcnf
    else:
        relations_4nf = decompose_to_4nf(ensure_dict_format(relations_bcnf))
        print("AFTER 4NF NORMALIZATION")
        for rel in relations_4nf.values():
            rel.display()
            print(rel.build_schema())
        print("-----------------------------------------------------------------------------------------------------------------")

    if choice == 5:
        return

    # Decompose to 5NF
    print("5NF")
    if check_all_relations_5nf(ensure_dict_format(relations_4nf)):
        print("RELATIONS ARE ALREADY IN 5NF")
    else:
        relations_5nf = decompose_to_5nf(list(ensure_dict_format(relations_4nf).values()))
        print("AFTER 5NF NORMALIZATION")
        for rel in relations_5nf:
            rel.display()
            print(rel.build_schema())

import subprocess
import sys

def install_requirements():
    """Installs packages from requirements.txt."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)


# if __name__ == "__main__":
install_requirements()
main()


#5NF Decomposition for new input
file_path = 'relation.xlsx'
df = pd.read_excel(file_path)
# Extract headers and data
headers = list(df.columns)
data = df.values.tolist()
primary_key = ['AttendeeID',	'SessionID',	'Location',	'PresentationType']
# Create Relation instance
relation = Relation(headers, data, primary_key)
relation.add_name("attendance")
print("Input Relation :")
print(relation.display())


# Decompose into 5NF relations if applicable
r1, r2 = decompose_to_5nf_relation_ip(relation)

if r1 and r2:
        print("Decomposition Successful! Relations in 5NF:")
        r1.display()
        r2.display()
else:
        print("No valid join dependencies detected. Relation is already in 5NF.")


