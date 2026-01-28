from enum import Enum

class WhereConstraintType(Enum):
    # CLASSIC = "WHERE conditions"
    # STRING = "WHERE STRING conditions"
    # EMPTY = "WHERE EMPTY conditions"
    # NULL = "WHERE NULL conditions"
    # NOT_NULL = "WHERE NOT NULL conditions"
    MULTIPLE = "MULTIPLE WHERE conditions"
    NESTED = "NESTED WHERE conditions"
    # WILDCARD = "WHERE conditions with WILDCARD that must have minimum 4 letters"
    # NO_WILDCARD = "WHERE conditions without WILDCARD"
    # EXIST = "EXIST in WHERE conditions"
    # NOT_EXIST = "NOT EXIST in WHERE conditions"
    # EXIST_OR_IN = "EXIST and NOT EXIST or IN and NOT IN into WHERE conditions"
    # NOT = "NOT in WHERE conditions"
    # COMPARISON_OPERATORS = "COMPARISON OPERATORS in WHERE conditions"
    ANY_ALL_IN = "ANY or ALL or IN in WHERE conditions"
    # HAVING = "WHERE or HAVING conditions"