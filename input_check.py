from datetime import date

from question import QuestionType, Precision



def is_float_like(n: str) -> bool:
    try:
        float(n)
        return True
    except:
        return False

def is_int_like(n: str) -> bool:
    try:
        int(n)
        return True
    except:
        return False

def is_iso_date_like(n: str) -> bool:
    try:
        date.fromisoformat(n)
        return True
    except:
        return False

def is_question_ok(typ, question, answer, precision, points):
    typ_ok = isinstance(typ, QuestionType)
    precision_ok = not precision or isinstance(precision, Precision)
    points_ok = not points or is_int_like(points)
    question_ok = isinstance(question, str)
    if typ_ok and precision_ok and question_ok and points_ok:
        return is_answer_ok(typ, answer)
    return False

def is_answer_ok(typ, answer):
    match typ:
        case QuestionType.DATE: return is_iso_date_like(answer)
        case QuestionType.FLOAT: return is_float_like(answer)
        case QuestionType.INT: return is_int_like(answer)
        case QuestionType.SET: return isinstance(answer, set)
        case QuestionType.STRING: return isinstance(answer, str)
        case _: raise NotImplementedError(f"Unknown question type: {typ}")
