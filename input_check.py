from datetime import date
from question_type import QuestionType
from question_precision import Precision

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

def is_question_ok(typ, question, answer, prec, pts):
    typ_ok = isinstance(typ, QuestionType)
    prec_ok = True if not prec or isinstance(prec, Precision) else False
    pts_ok = True if not pts or is_int_like(pts) else False
    question_ok = isinstance(question, str)
    if typ_ok and prec_ok and question_ok and pts_ok:
        return is_answer_ok(typ, answer)
    return False

def is_answer_ok(typ, answer):
    match typ:
        case QuestionType.DATE: return is_iso_date_like(answer)
        case QuestionType.FLOAT: return is_float_like(answer)
        case QuestionType.INT: return is_int_like(answer)
        case QuestionType.SET: return isinstance(answer, set)
        case _: raise NotImplementedError(f"Unknown question type: {typ}")


