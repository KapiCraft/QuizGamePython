from enum import Enum

class QuestionType(Enum):
    INT = 1
    STRING = 2
    SET = 3
    DATE = 4
    FLOAT = 5

class Precision(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2