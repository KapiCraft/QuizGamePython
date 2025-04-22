from datetime import date

from question_enums import QuestionType, Precision



def looks_like_float(n: str) -> bool:
    try:
        float(n)
        return True
    except:
        return False

def looks_like_int(n: str) -> bool:
    try:
        int(n)
        return True
    except:
        return False

def looks_like_iso_date(n: str) -> bool:
    try:
        date.fromisoformat(n)
        return True
    except:
        return False

def looks_like_question(typ, question, answer, precision, points):
    typ_ok = isinstance(typ, QuestionType)
    precision_ok = not precision or isinstance(precision, Precision)
    points_ok = not points or looks_like_int(points)
    question_ok = isinstance(question, str)
    if typ_ok and precision_ok and question_ok and points_ok:
        return looks_like_answer(typ, answer)
    return False

def looks_like_answer(typ, answer):
    match typ:
        case QuestionType.DATE: return looks_like_iso_date(answer)
        case QuestionType.FLOAT: return looks_like_float(answer)
        case QuestionType.INT: return looks_like_int(answer)
        case QuestionType.SET: return isinstance(answer, set)
        case QuestionType.STRING: return isinstance(answer, str)
        case _: raise NotImplementedError(f"Unknown question type: {typ}")
