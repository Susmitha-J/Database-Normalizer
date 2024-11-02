
import pandas as pd
from Relation import Relation
from Dependency import Dependency

# Normalization checks and decomposition functions

def is_1nf(relation):
    """
    Checks if the data in the relation is in the First Normal Form (1NF).

    Parameters:
        relation (Relation): The base Relation instance.

    Returns:
        bool: True if the relation is in 1NF, False otherwise.
        list: A list of attributes that are not in 1NF (have multivalued entries).
    """
    non_1nf_columns = set()

    # Check each row to see if any column has multivalued entries
    for row in relation.data:
        for index, value in enumerate(row):
            # Consider a multivalued attribute if there are commas in the value
            if isinstance(value, str) and ',' in value:
                non_1nf_columns.add(relation.headers[index])

    # If there are any columns identified, it is not in 1NF
    is_in_1nf = len(non_1nf_columns) == 0
    return is_in_1nf, list(non_1nf_columns)


def is_2nf(relation):
    """
    Checks if the relation is in Second Normal Form (2NF).

    Parameters:
        relation (Relation): The relation instance to check.

    Returns:
        bool: True if the relation is in 2NF, False otherwise.
    """
    # Step 1: Check if the relation is in 1NF
    if not is_1nf(relation):
        return False

    # Step 2: Check for partial dependencies
    primary_key = relation.primary_key
    non_prime_attributes = [attr for attr in relation.headers if attr not in primary_key]

    # If the primary key is a single attribute, it cannot have partial dependencies
    if len(primary_key) == 1:
        return True

    # Look for partial dependencies: Non-prime attribute dependent on part of the composite primary key
    for dep in relation.dependencies:
        lhs_set = set(dep.lhs)
        rhs_set = set(dep.rhs)

        # Check if it's a partial dependency
        if lhs_set.issubset(set(primary_key)) and lhs_set != set(primary_key):
            # If RHS contains non-prime attributes, it's a partial dependency
            if any(attr in non_prime_attributes for attr in rhs_set):
                return False

    # If no partial dependencies are found, it's in 2NF
    return True

def check_all_relations_2nf(relations):
    """
    Checks if all relations in the dictionary are in 2NF and prints the results.

    Parameters:
        relations (dict): Dictionary of relation names to Relation objects.
    """
    for name, relation in relations.items():
        if is_2nf(relation):
            continue
        else:
            return False
    return True



def is_3nf(relation):
    """
    Checks if the relation is in Third Normal Form (3NF).

    Parameters:
        relation (Relation): The relation instance to check.

    Returns:
        bool: True if the relation is in 3NF, False otherwise.
    """
    # Step 1: Check if the relation is in 2NF
    if not is_2nf(relation):
        return False

    primary_key = set(relation.primary_key)
    candidate_keys = [set(relation.primary_key)]  # Assuming the primary key is the candidate key
    non_prime_attributes = [attr for attr in relation.headers if attr not in primary_key]

    # Step 2: Check for transitive dependencies
    for dep in relation.dependencies:
        lhs_set = set(dep.lhs)
        rhs_set = set(dep.rhs)

        # Check if the dependency violates 3NF conditions
        if not lhs_set.issuperset(primary_key) and not any(attr in primary_key for attr in rhs_set):
            # If LHS is not a superkey and RHS has non-prime attributes, it's a transitive dependency
            if any(attr in non_prime_attributes for attr in rhs_set):
                return False

    # If no transitive dependencies are found, it's in 3NF
    return True

def check_all_relations_3nf(relations):
    """
    Checks if all relations in the dictionary are in 3NF and prints the results.

    Parameters:
        relations (dict): Dictionary of relation names to Relation objects.
    """
    flag = True
    for name, relation in relations.items():
        if is_3nf(relation):
            continue
        else:
            flag = False
    return flag


def is_superkey(relation, lhs_set):
    """
    Checks if the given set of attributes (lhs_set) is a superkey for the relation.

    Parameters:
        relation (Relation): The relation to check against.
        lhs_set (set): The set of attributes to determine if it is a superkey.

    Returns:
        bool: True if lhs_set is a superkey, False otherwise.
    """
    primary_key_set = set(relation.primary_key)
    return lhs_set.issuperset(primary_key_set)

def is_bcnf(relation):
    """
    Checks if the relation is in Boyce-Codd Normal Form (BCNF).

    Parameters:
        relation (Relation): The relation instance to check.

    Returns:
        bool: True if the relation is in BCNF, False otherwise.
    """
    # Step 1: Check if the relation is in 3NF
    if not is_3nf(relation):
        return False

    # Step 2: Check for BCNF compliance
    for dep in relation.dependencies:
        lhs_set = set(dep.lhs)
        # Check if the left-hand side is a superkey
        if not is_superkey(relation, lhs_set) and  not dep.dependency_type == "MVD":
            return False

    # If no violations are found, it's in BCNF
    return True

def check_all_relations_bcnf(relations):
    """
    Checks if all relations in the dictionary are in BCNF and prints the results.

    Parameters:
        relations (dict): Dictionary of relation names to Relation objects.
    """
    flag = True
    for name, relation in relations.items():
        if is_bcnf(relation):
            continue
        else:
            flag = False
    return flag

def is_4nf(relation):
    """
    Checks if the relation is in Fourth Normal Form (4NF).

    Parameters:
        relation (Relation): The relation instance to check.

    Returns:
        bool: True if the relation is in 4NF, False otherwise.
    """
    # Ensure the relation is in BCNF first
    if not is_bcnf(relation):
        return False

    # Check for non-trivial MVDs
    for dep in relation.dependencies:
        lhs_set = set(dep.lhs)
        if dep.dependency_type == "MVD" and not is_superkey(relation, lhs_set):
            # Found a 4NF violation due to a non-trivial MVD
            return False
    return True

def check_all_relations_4nf(relations):
    """
    Checks if all relations in the dictionary are in 4NF and prints the results.

    Parameters:
        relations (dict): Dictionary of relation names to Relation objects.
    """
    flag = True
    for name, relation in relations.items():
        if is_4nf(relation):
            pass
        else:
            flag = False
    return flag

def extract_5nf_data(relation, subset, complement_set):
    """
    Extracts data for potential 5NF decomposition based on a subset and its complement.

    Parameters:
        relation (Relation): The base relation instance.
        subset (list): The subset of attributes to extract data for.
        complement_set (list): The complement of the subset.

    Returns:
        tuple: Two lists of data, one for each part of the potential decomposition.
    """
    # Indices of the subset and complement attributes in the original relation
    subset_indices = [relation.headers.index(attr) for attr in subset]
    complement_indices = [relation.headers.index(attr) for attr in complement_set]

    # Extract the two sets of data
    data_1 = []
    data_2 = []

    # Track unique rows for data_1 and data_2
    existing_data_1 = set()
    existing_data_2 = set()

    for row in relation.data:
        # Extract rows based on the subset and complement set
        row_1 = tuple(row[idx] for idx in subset_indices)
        row_2 = tuple(row[idx] for idx in complement_indices)

        if row_1 not in existing_data_1:
            data_1.append(list(row_1))
            existing_data_1.add(row_1)

        if row_2 not in existing_data_2:
            data_2.append(list(row_2))
            existing_data_2.add(row_2)

    return data_1, data_2

def check_all_relations_5nf(relations):
    """
    Check if all given relations are in 5NF.

    Parameters:
        relations (dict): A dictionary of Relation instances.

    Returns:
        bool: True if all relations are in 5NF, False otherwise.
    """
    all_in_5nf = True
    for name, relation in relations.items():
        if is_5nf(relation):
            pass
        else:
            all_in_5nf = False
    return all_in_5nf

def generate_possible_subsets(attributes):
    """
    Generate possible subsets of attributes for join dependency detection.

    Parameters:
        attributes (list): List of attributes in the relation.

    Returns:
        list: List of potential subsets.
    """
    from itertools import combinations

    # Generate non-trivial subsets (at least 2 elements, less than the total length)
    return [list(combo) for i in range(2, len(attributes)) for combo in combinations(attributes, i)]

def is_5nf(relation):
    """
    Determine if the given relation is in 5NF by checking for valid join dependencies.

    Parameters:
        relation (Relation): The base Relation instance.

    Returns:
        bool: True if the relation is in 5NF, False otherwise.
    """
    join_dependencies = detect_valid_join_dependencies(relation)
    return len(join_dependencies) == 0

def detect_valid_join_dependencies(relation):
    """
    Detect valid join dependencies for 5NF decomposition.

    Parameters:
        relation (Relation): The Relation instance.

    Returns:
        list: List of join dependencies if they exist, otherwise empty.
    """
    detected_jds = []
    subsets = generate_possible_subsets(relation.headers)

    for subset in subsets:
        complement_set = list(set(relation.headers) - set(subset))
        # Ensure the subsets are non-trivial
        if len(subset) >= 2 and len(complement_set) >= 2:
            # Attempt to decompose based on these attributes
            if can_be_decomposed(subset, relation):
                detected_jds.append({'decomposition': (subset, complement_set)})

    return detected_jds

def can_be_decomposed(subset, relation):
    """
    Checks if the relation can be decomposed based on the subset attributes (join dependency check).

    Parameters:
        subset (list): Subset of attributes to check for join dependency.
        relation (Relation): The base relation.

    Returns:
        bool: True if the relation can be decomposed using this subset, False otherwise.
    """
    complement_set = list(set(relation.headers) - set(subset))
    data_1, data_2 = extract_5nf_data(relation, subset, complement_set)

    # Simulate a natural join
    rejoined_data = simulate_natural_join(data_1, data_2, subset, complement_set)
    original_data_set = set(tuple(row) for row in relation.data)
    rejoined_data_set = set(tuple(row) for row in rejoined_data)

    # Ensure that the data can be decomposed, and prevent trivial decomposition (single columns)
    return original_data_set == rejoined_data_set and len(data_1[0]) > 1 and len(data_2[0]) > 1

def extract_5nf_data(relation, subset, complement_set):
    """
    Extracts data for potential 5NF decomposition based on a subset and its complement.

    Parameters:
        relation (Relation): The base relation instance.
        subset (list): The subset of attributes to extract data for.
        complement_set (list): The complement of the subset.

    Returns:
        tuple: Two lists of data, one for each part of the potential decomposition.
    """
    subset_indices = [relation.headers.index(attr) for attr in subset]
    complement_indices = [relation.headers.index(attr) for attr in complement_set]

    data_1, data_2 = [], []
    existing_data_1, existing_data_2 = set(), set()

    for row in relation.data:
        row_1 = tuple(row[idx] for idx in subset_indices)
        row_2 = tuple(row[idx] for idx in complement_indices)

        if row_1 not in existing_data_1:
            data_1.append(list(row_1))
            existing_data_1.add(row_1)

        if row_2 not in existing_data_2:
            data_2.append(list(row_2))
            existing_data_2.add(row_2)

    return data_1, data_2

def simulate_natural_join(data_1, data_2, subset, complement_set):
    """
    Simulate a natural join between two datasets based on join attributes.

    Parameters:
        data_1 (list): Data extracted from the first subset.
        data_2 (list): Data extracted from the complement subset.
        subset (list): Attributes used in the first dataset.
        complement_set (list): Attributes used in the second dataset.

    Returns:
        list: Resulting joined dataset.
    """
    joined_data = []

    for row1 in data_1:
        for row2 in data_2:
            # Match on overlapping attributes (intersecting columns)
            join_attributes = list(set(subset).intersection(complement_set))
            if all(row1[subset.index(attr)] == row2[complement_set.index(attr)] for attr in join_attributes):
                # Combine rows ensuring no duplicates
                combined_row = row1 + [row2[complement_set.index(attr)] for attr in complement_set if attr not in join_attributes]
                joined_data.append(combined_row)

    return joined_data


def detect_join_dependency_ip(relation):
    """
    Detect join dependencies for 5NF decomposition.
    Based on the given business rule and dataset structure.
    Uses Relation class instead of data frames directly.
    """
    r1_columns = ['SessionID',	'Location',	'PresentationType']
    r2_columns = ['AttendeeID',	'SessionID',	'Location']

    # Convert the relation data into a pandas DataFrame
    data = pd.DataFrame(relation.data, columns=relation.headers)

    # Extract data for R1 and R2 based on column sets and drop duplicates
    r1_data = data[r1_columns].drop_duplicates().reset_index(drop=True)
    r2_data = data[r2_columns].drop_duplicates().reset_index(drop=True)


    # Perform a natural join on DrinkID and check if the result matches the original data
    merged_data = pd.merge(r1_data, r2_data, on=['SessionID', 'Location'], how='inner')
    original_data = pd.DataFrame(relation.data, columns=relation.headers)

    merged_data_aligned = merged_data[original_data.columns]

    # Compare the aligned merged data to the original data
    if merged_data_aligned.equals(original_data):
        return r1_columns, r2_columns
    return None, None

def decompose_to_5nf_relation_ip(base_relation):
    """
    Decompose a Relation instance into 5NF if a valid join dependency is detected.
    """
    # Detect join dependency using the updated function for Relation
    r1_columns, r2_columns = detect_join_dependency_ip(base_relation)

    if r1_columns and r2_columns:
        # Convert the relation data into a pandas DataFrame
        data = pd.DataFrame(base_relation.data, columns=base_relation.headers)

        # Extract data for R1 and R2 based on detected join dependencies and drop duplicates
        r1_data = data[r1_columns].drop_duplicates().values.tolist()
        r2_data = data[r2_columns].drop_duplicates().values.tolist()

        # Define primary keys for the decomposed relations
        r1_primary_key = ['SessionID',	'Location',	'PresentationType']
        r2_primary_key = ['AttendeeID',	'SessionID',	'Location']

        # Create Relation instances for R1 and R2
        r1_relation = Relation(r1_columns, r1_data, primary_key=r1_primary_key)
        r2_relation = Relation(r2_columns, r2_data, primary_key=r2_primary_key)

        # Assign names to the new relations
        r1_relation.add_name("Table1")
        r2_relation.add_name("Table2")

        return r1_relation, r2_relation
    return None, None

def normalize_1nf_relation(relation, multivalued_attributes):
    """
    Normalize the base relation to 1NF by creating separate relations for multivalued attributes.

    Parameters:
        relation (Relation): The base Relation instance.
        multivalued_attributes (list): List of multivalued attribute names to normalize.

    Returns:
        dict: A dictionary with the base relation and new Relation instances for each multivalued attribute.
    """
    # Indices for primary keys and multivalued attributes
    pk_indices = [relation.headers.index(pk) for pk in relation.primary_key]
    mv_indices = {attr: relation.headers.index(attr) for attr in multivalued_attributes if attr in relation.headers}

    # Base relation without multivalued attributes
    base_headers = [h for h in relation.headers if h not in multivalued_attributes]
    base_data = [[row[i] for i, h in enumerate(relation.headers) if h not in multivalued_attributes] for row in relation.data]

    # Create the base relation without multivalued attributes
    base_relation = Relation(base_headers, base_data, relation.primary_key)
    base_relation.add_name("BaseRelation")  # Use add_name method for the base relation

    # Relations for each multivalued attribute
    new_relations = {}
    for attr, idx in mv_indices.items():
        new_relation_headers = relation.primary_key + [attr]
        new_relation_data = []
        for row in relation.data:
            values = str(row[idx]).split(',')
            for value in values:
                new_row = [row[i] for i in pk_indices] + [value.strip()]
                new_relation_data.append(new_row)

        # Create new Relation instance and set its name using add_name
        new_relation = Relation(new_relation_headers, new_relation_data, relation.primary_key + [attr])
        new_relation.add_name(attr)  # Assign the name based on the multivalued attribute

        # Add foreign key references to the primary key of the base relation
        for pk in relation.primary_key:
            new_relation.add_foreign_key((pk, base_relation.name, pk))

        new_relations[attr] = new_relation

    return {
        "BaseRelation": base_relation,
        **new_relations
    }

def decompose_to_2nf(relations):
    new_relations = {}  # To store the new normalized relations

    for table_name, relation in relations.items():
        primary_key = set(relation.primary_key)
        partial_deps = []
        full_deps = []
        transitive_deps = []
        mvd_deps = []

        # Separate partial dependencies, full dependencies, and potential transitive dependencies
        for dep in relation.dependencies:
            lhs_set = set(dep.lhs)
            if dep.dependency_type == 'FD' and lhs_set.issubset(primary_key) and lhs_set != primary_key:
                  if dep.is_partial_dependency():
                        partial_deps.append(dep)
                  else:
                        full_deps.append(dep)
            elif not lhs_set.issubset(primary_key):
                  # Dependencies where LHS is not a subset of primary key might be transitive
                  transitive_deps.append(dep)
            elif dep.dependency_type == 'MVD':
                  mvd_deps.append(dep)


        # If there are partial dependencies, decompose the relation
        if partial_deps:
            # Create a new relation for each partial dependency
            for partial_dep in partial_deps:
                new_table_name = f"{table_name}_Partial_{len(new_relations) + 1}"
                new_headers = list(set(partial_dep.lhs + partial_dep.rhs))
                new_data = []
                new_primary_key = partial_dep.lhs  # Use the LHS as the new primary key
                rhs_in_primary_key = any(attr in primary_key for attr in partial_dep.rhs)
                if rhs_in_primary_key:
                    # If RHS has original primary key attributes, keep the original composite key
                    new_primary_key = list(set(partial_dep.lhs + partial_dep.rhs))
                else:
                    new_primary_key = partial_dep.lhs

                # Extract unique values for the new relation
                existing_rows = set()
                for row in relation.data:
                    new_row = [row[relation.headers.index(attr)] for attr in new_headers]
                    if tuple(new_row) not in existing_rows:
                        new_data.append(new_row)
                        existing_rows.add(tuple(new_row))

                # Create a new relation object for the partial dependency
                new_relation = Relation(new_headers, new_data, new_primary_key)
                new_relation.add_name(new_table_name)

                # Ensure the partial dependency is added as a new dependency
                new_dep = Dependency(f"{','.join(partial_dep.lhs)} -> {','.join(partial_dep.rhs)}", [new_primary_key])
                new_relation.add_dependency(new_dep)

                # Add foreign key references to the original relation's primary key
                for pk in relation.primary_key:
                    if pk in new_headers and pk not in new_primary_key:
                        new_relation.add_foreign_key((pk, table_name, pk))

                # Also check for transitive dependencies that should be added
                for trans_dep in transitive_deps:
                    if all(attr in new_headers for attr in trans_dep.lhs + trans_dep.rhs):
                        new_relation.add_dependency(trans_dep)

                new_relations[new_table_name] = new_relation

            # Create the original table with remaining attributes after decomposition
            remaining_headers = list(set(relation.headers) - set(sum([dep.rhs for dep in partial_deps], [])))
            remaining_data = []

            # Update the primary key for the remaining relation
            remaining_primary_key = list(set(primary_key).intersection(remaining_headers))
            if not remaining_primary_key:
                # If none of the original primary key attributes remain, use the original primary key
                remaining_primary_key = relation.primary_key

            # Update the remaining dependencies, including transitive ones
            remaining_dependencies = []
            for dep in full_deps + transitive_deps + mvd_deps:
                if all(attr in remaining_headers for attr in dep.lhs + dep.rhs):
                    # Ensure candidate keys are properly updated and add to the remaining dependencies
                    dep.candidate_keys = [remaining_primary_key]
                    remaining_dependencies.append(dep)

            existing_rows = set()
            for row in relation.data:
                new_row = [row[relation.headers.index(attr)] for attr in remaining_headers]
                if tuple(new_row) not in existing_rows:
                    remaining_data.append(new_row)
                    existing_rows.add(tuple(new_row))

            # Update the original relation
            new_relation = Relation(remaining_headers, remaining_data, remaining_primary_key)
            new_relation.add_name(table_name)
            new_relation.dependencies = remaining_dependencies

            # Ensure the new original relation retains foreign keys to its decomposed parts if needed
            for partial_relation_name, partial_relation in new_relations.items():
                for pk in partial_relation.primary_key:
                    if pk in remaining_headers and pk not in remaining_primary_key:
                        new_relation.add_foreign_key((pk, partial_relation_name, pk))

            new_relations[table_name] = new_relation

        else:
            # No partial dependencies, keep the original relation
            new_relations[table_name] = relation

    return new_relations

def track_primary_keys(relations):
    """
    Creates a dictionary that maps primary key attributes to their originating tables.
    This is used to determine foreign key relationships during decomposition.

    Parameters:
        relations (dict): Dictionary of relation names to Relation objects.

    Returns:
        dict: Mapping of primary key attributes to their source table names.
    """
    primary_key_map = {}
    for table_name, relation in relations.items():
        for pk in relation.primary_key:
            primary_key_map[pk] = table_name
    return primary_key_map

def decompose_to_3nf(relations):
    # Track the original primary keys and their source tables
    primary_key_map = track_primary_keys(relations)
    new_relations = {}  # To store the new normalized relations

    for table_name, relation in relations.items():
        primary_key = set(relation.primary_key)
        transitive_deps = []
        non_transitive_deps = []

        # Separate transitive dependencies and non-transitive dependencies
        for dep in relation.dependencies:
            lhs_set = set(dep.lhs)
            rhs_set = set(dep.rhs)

            # A transitive dependency occurs if the LHS is not a superkey and the RHS is a non-prime attribute
            if not lhs_set.issuperset(primary_key) and not any(attr in primary_key for attr in rhs_set):
                transitive_deps.append(dep)
            else:
                non_transitive_deps.append(dep)

        # Create new relations for transitive dependencies
        for trans_dep in transitive_deps:
            # Create a new relation for each transitive dependency
            new_table_name = f"{table_name}_Transitive_{len(new_relations) + 1}"
            new_headers = list(set(trans_dep.lhs + trans_dep.rhs))
            new_data = []
            new_primary_key = trans_dep.lhs  # Use the LHS as the new primary key

            # Extract unique values for the new relation
            existing_rows = set()
            for row in relation.data:
                new_row = [row[relation.headers.index(attr)] for attr in new_headers]
                if tuple(new_row) not in existing_rows:
                    new_data.append(new_row)
                    existing_rows.add(tuple(new_row))

            # Create a new relation object for the transitive dependency
            new_relation = Relation(new_headers, new_data, new_primary_key)
            new_relation.add_name(new_table_name)

            # Ensure the transitive dependency is added as a new dependency
            new_dep = Dependency(f"{','.join(trans_dep.lhs)} -> {','.join(trans_dep.rhs)}", [new_primary_key])
            new_relation.add_dependency(new_dep)

            # Add foreign key references based on the original source of the attribute
            for attr in new_headers:
                if attr in primary_key_map and attr not in new_primary_key:
                    source_table = primary_key_map[attr]
                    new_relation.add_foreign_key((attr, source_table, attr))

            new_relations[new_table_name] = new_relation

        # Adjust the original relation by removing transitive dependencies
        if transitive_deps:
            remaining_headers = list(set(relation.headers) - set(sum([dep.rhs for dep in transitive_deps], [])))
            remaining_data = []

            # Determine the new primary key, keeping it as close to the original as possible
            remaining_primary_key = list(set(primary_key).intersection(remaining_headers))
            if not remaining_primary_key:
                # If none of the original primary key attributes remain, use the original primary key
                remaining_primary_key = relation.primary_key

            # Update the remaining dependencies, excluding the transitive ones
            remaining_dependencies = []
            for dep in non_transitive_deps:
                if all(attr in remaining_headers for attr in dep.lhs + dep.rhs):
                    dep.candidate_keys = [remaining_primary_key]
                    remaining_dependencies.append(dep)

            existing_rows = set()
            for row in relation.data:
                new_row = [row[relation.headers.index(attr)] for attr in remaining_headers]
                if tuple(new_row) not in existing_rows:
                    remaining_data.append(new_row)
                    existing_rows.add(tuple(new_row))

            # Create the updated original relation
            new_relation = Relation(remaining_headers, remaining_data, remaining_primary_key)
            new_relation.add_name(table_name)
            new_relation.dependencies = remaining_dependencies

            # Ensure the new original relation retains foreign keys based on tracked primary keys
            for attr in remaining_headers:
                if attr in primary_key_map and attr not in remaining_primary_key:
                    source_table = primary_key_map[attr]
                    new_relation.add_foreign_key((attr, source_table, attr))

            new_relations[table_name] = new_relation

        else:
            # No transitive dependencies, keep the original relation
            new_relations[table_name] = relation

    return new_relations


def remove_duplicate_relations(relations):
    """
    Removes duplicate relations based on identical primary keys and headers.

    Parameters:
        relations (dict): A dictionary of relation names to Relation objects.

    Returns:
        dict: A dictionary of unique relations.
    """
    unique_relations = {}
    seen_primary_keys = {}

    for name, relation in relations.items():
        # Create a key from primary key attributes and sorted headers to identify uniqueness
        primary_key_tuple = (tuple(sorted(relation.primary_key)), tuple(sorted(relation.headers)))

        if primary_key_tuple not in seen_primary_keys:
            seen_primary_keys[primary_key_tuple] = name
            unique_relations[name] = relation
        else:
            # Optionally, you can print which relations are being considered duplicates and skipped
            pass
    return unique_relations


def decompose_to_bcnf(relations):
    """
    Normalize the given relations to BCNF, if needed.

    Parameters:
        relations (dict): Dictionary of relation names to Relation objects.

    Returns:
        dict: A dictionary with the relations normalized to BCNF.
    """
    # Check if all relations are already in BCNF
    if check_all_relations_bcnf(relations):
        return relations  # If satisfied, return the original relations

    # Track the original primary keys and their source tables
    primary_key_map = track_primary_keys(relations)
    new_relations = {}  # To store the new normalized relations
    relation_queue = list(relations.items())  # Use a queue to keep track of relations to process

    while relation_queue:
        table_name, relation = relation_queue.pop(0)
        primary_key = set(relation.primary_key)
        bcnf_violations = []

        # Identify BCNF violations: dependencies where LHS is not a superkey
        for dep in relation.dependencies:
            lhs_set = set(dep.lhs)
            if not is_superkey(relation, lhs_set):
                bcnf_violations.append(dep)

        if bcnf_violations:
            # Handle the first BCNF violation
            violating_dep = bcnf_violations[0]
            lhs_attributes = violating_dep.lhs
            rhs_attributes = violating_dep.rhs

            # Create a new relation for the BCNF violation
            new_table_name = f"{table_name}_BCNF_{len(new_relations) + 1}"
            new_headers = list(set(lhs_attributes + rhs_attributes))
            new_data = []
            new_primary_key = lhs_attributes

            # Extract unique values for the new relation
            existing_rows = set()
            for row in relation.data:
                new_row = [row[relation.headers.index(attr)] for attr in new_headers]
                if tuple(new_row) not in existing_rows:
                    new_data.append(new_row)
                    existing_rows.add(tuple(new_row))

            # Create a new relation object for the BCNF violation
            new_relation = Relation(new_headers, new_data, new_primary_key)
            new_relation.add_name(new_table_name)
            new_dep = Dependency(f"{','.join(lhs_attributes)} -> {','.join(rhs_attributes)}", [new_primary_key])
            new_relation.add_dependency(new_dep)

            # Add foreign key references based on the original source of the attribute
            for attr in new_headers:
                if attr in primary_key_map and attr not in new_primary_key:
                    source_table = primary_key_map[attr]
                    new_relation.add_foreign_key((attr, source_table, attr))

            new_relations[new_table_name] = new_relation

            # Adjust the original relation to remove the violating attributes
            remaining_headers = list(set(relation.headers) - set(rhs_attributes) | set(lhs_attributes))
            remaining_data = []
            remaining_primary_key = relation.primary_key

            # Extract the remaining data
            existing_rows = set()
            for row in relation.data:
                new_row = [row[relation.headers.index(attr)] for attr in remaining_headers]
                if tuple(new_row) not in existing_rows:
                    remaining_data.append(new_row)
                    existing_rows.add(tuple(new_row))

            # Update the original relation
            updated_relation = Relation(remaining_headers, remaining_data, remaining_primary_key)
            updated_relation.add_name(table_name)

            # If this updated relation still has BCNF violations, add it back to the queue
            relation_queue.append((table_name, updated_relation))

        else:
            # No BCNF violations, the relation is good as it is
            new_relations[table_name] = relation
            print(f"Relation '{table_name}' is already in BCNF.")

    return new_relations


def decompose_to_4nf(relations):
    new_relations = {}
    processed_tables = set()

    for table_name, relation in relations.items():
        primary_key = set(relation.primary_key)
        mvd_violations = []

        # Detect MVDs in the relation
        for dep in relation.dependencies:
            lhs_set = set(dep.lhs)
            rhs_set = set(dep.rhs)

            # Identify MVDs where LHS is not a superkey
            if dep.dependency_type == "MVD" and not is_superkey(relation, lhs_set):
                mvd_violations.append(dep)

        if mvd_violations:
            # Handle MVDs by creating a new relation for each attribute in RHS
            for mvd in mvd_violations:
                lhs = mvd.lhs
                rhs = mvd.rhs

                # Create a new relation for each RHS attribute individually
                for rhs_attr in rhs:
                    new_table_name = f"{table_name}_4NF_{len(new_relations) + 1}_Part_{rhs_attr}"
                    new_headers = lhs + [rhs_attr]
                    new_data = []

                    # Extract unique values for the new relation
                    existing_rows = set()
                    for row in relation.data:
                        new_row = [row[relation.headers.index(attr)] for attr in new_headers]
                        if tuple(new_row) not in existing_rows:
                            new_data.append(new_row)
                            existing_rows.add(tuple(new_row))

                    # Create the new relation for the attribute
                    new_relation = Relation(new_headers, new_data, lhs + [rhs_attr])
                    new_relation.add_name(new_table_name)
                    new_relations[new_table_name] = new_relation

            # Adjust the original relation by removing the decomposed RHS attributes
            remaining_headers = list(set(relation.headers) - set(rhs))
            remaining_data = []
            existing_rows = set()

            for row in relation.data:
                new_row = [row[relation.headers.index(attr)] for attr in remaining_headers]
                if tuple(new_row) not in existing_rows:
                    remaining_data.append(new_row)
                    existing_rows.add(tuple(new_row))

            # Create the remaining relation if there are significant attributes left
            if len(remaining_headers) > len(relation.primary_key):
                updated_relation_name = f"{table_name}_Remaining"
                updated_relation = Relation(remaining_headers, remaining_data, relation.primary_key)
                updated_relation.add_name(updated_relation_name)
                new_relations[updated_relation_name] = updated_relation
                processed_tables.add(updated_relation_name)

        else:
            # If there are no MVD violations, keep the original relation
            new_relations[table_name] = relation
    new_relations = remove_duplicate_relations(new_relations)
    return new_relations


def decompose_to_5nf(relations):
    """
    Decompose given relations to 5NF based on detected join dependencies.

    Parameters:
        relations (list): List of Relation instances.

    Returns:
        list: List of normalized Relation instances in 5NF.
    """
    decomposed_relations = []

    for relation in relations:
        # Step 1: Check if the relation is already in 5NF
        if is_5nf(relation):
            decomposed_relations.append(relation)
            continue

        # Step 2: Detect join dependencies for potential 5NF violations
        join_dependencies = detect_valid_join_dependencies(relation)

        # If there are no valid join dependencies, it is already in 5NF
        if not join_dependencies:
            decomposed_relations.append(relation)
            continue

        # Step 3: Decompose based on the detected join dependencies
        for jd in join_dependencies:
            subset1, subset2 = jd['decomposition']

            # Extract data for each subset
            data_1, data_2 = extract_5nf_data(relation, subset1, subset2)

            # Create new Relation instances for the decomposed parts
            relation1 = Relation(subset1, data_1, primary_key=subset1)
            relation1_name = f"{relation.name}_PartA"
            relation1.add_name(relation1_name)
            decomposed_relations.append(relation1)

            relation2 = Relation(subset2, data_2, primary_key=subset2)
            relation2_name = f"{relation.name}_PartB"
            relation2.add_name(relation2_name)
            decomposed_relations.append(relation2)

            print(f"Decomposed '{relation.name}' into '{relation1_name}' and '{relation2_name}'.")

    return decomposed_relations