
class Dependency:
    def __init__(self, dependency_str, candidate_keys):
        """
        Initializes the dependency with the given string and the candidate keys.
        :param dependency_str: The functional/multivalued dependency as a string.
        :param candidate_keys: List of lists, each list representing a candidate key.
        """
        self.dependency_str = dependency_str.strip()
        self.candidate_keys = candidate_keys
        self.lhs = []
        self.rhs = []
        self.dependency_type = ""
        self.parse_dependency()

    def parse_dependency(self):
        """
        Parses the dependency string and separates lhs (left-hand side) and rhs (right-hand side).
        Also identifies the type of dependency (FD or MVD).
        """
        # Multivalued Dependency (MVD) is represented by '-->>', FD by '->'
        if '-->>' in self.dependency_str:
            self.lhs, rhs_part = self.dependency_str.split('-->>')
            self.dependency_type = 'MVD'
        elif '->' in self.dependency_str:
            self.lhs, rhs_part = self.dependency_str.split('->')
            self.dependency_type = 'FD'
        else:
            raise ValueError("Invalid dependency format!")

        # Clean and split lhs and rhs by commas for multiple attributes
        self.lhs = [x.strip() for x in self.lhs.split(',')]
        self.rhs = [x.strip() for x in rhs_part.split(',')]

    def is_partial_dependency(self):
        """
        Checks if the dependency is a partial dependency.
        A partial dependency exists if lhs is a proper subset of a candidate key.
        :return: True if it's a partial dependency, False otherwise.
        """
        for candidate_key in self.candidate_keys:
            if  (set(self.lhs).issubset(set(candidate_key)) and set(self.lhs) != set(candidate_key)):
                return True
        return False

    def __str__(self):
        """
        String representation of the dependency.
        :return: Dependency in human-readable format.
        """
        return f"LHS: {self.lhs}, RHS: {self.rhs}, Type: {self.dependency_type}, Partial: {self.is_partial_dependency()}"
