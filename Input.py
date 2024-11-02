
from Dependency import Dependency

def read_dependencies_from_file(filename):
    dependencies = {}
    current_relation = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                current_relation = line[:-1]
                dependencies[current_relation] = []
            elif line:
                dependencies[current_relation].append(line)
    return dependencies

def validate_and_add_dependencies(relations, dependencies):
    for relation_name, fds in dependencies.items():
        relation = relations.get(relation_name)
        if not relation:
            print(f"Relation '{relation_name}' not found.")
            continue
        print(f"Dependencies for '{relation_name}': - ")
        for fd in fds:
            print(f"  - {fd}")
        user_input = input(f"Do you confirm all dependencies for '{relation_name}'? (yes/no): ").strip().lower()
        if user_input == "yes":
            for fd in fds:
                dependency = Dependency(fd, [relation.primary_key])
                relation.add_dependency(dependency)
            print(f"Dependencies added to relation '{relation_name}'.")
        else:
            print(f"Skipping dependencies for '{relation_name}'.")
        while user_input != "done":
            user_input = input(f"Enter additional dependency for '{relation_name}' in 'LHS -> RHS' or 'LHS -->> RHS' format (or 'done' to finish): ").strip()
            if user_input != "done":
                dependency = Dependency(user_input, [relation.primary_key])
                relation.add_dependency(dependency)
                print(f"Added dependency '{user_input}' to relation '{relation_name}'.")
    return relations
