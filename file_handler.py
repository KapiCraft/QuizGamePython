import pickle
from random import shuffle
from typing import List

import config
from question import Question, Precision
import input_check


def load_questions(shuffle_db: bool = True) -> List[Question]:
    try:
        with open(config.QUIZ_DB, "rb") as f:
            db = pickle.load(f)
            if shuffle_db:
                shuffle(db)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fájl nem található: {config.QUIZ_DB}")

    return [x for x in list(map(_create_question, db)) if x]       #removes None-s from db, as a result of failed _create_question

def _create_question(act) -> Question | None:
    if 3 <= len(act) <= 5:
        typ, quest, ans, *rest = act
        prec, pts = None, None
        for i in rest:
            if isinstance(i, Precision):
                prec = i
            elif input_check.is_int_like(i):
                pts = i
        if input_check.is_question_ok(typ=typ, question=quest, answer=ans, prec=prec, pts=pts):
            return Question(question=quest, answer=ans, questiontype=typ, precision=prec, points=pts)
    return None
