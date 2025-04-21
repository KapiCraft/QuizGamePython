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
        typ, question, answer, *rest = act
        precision, points = None, None
        for i in rest:
            if isinstance(i, Precision):
                precision = i
            elif input_check.looks_like_int(i):
                points = i
        if input_check.looks_like_question(typ=typ, question=question, answer=answer, precision=precision, points=points):
            return Question(question=question, answer=answer, questiontype=typ, precision=precision, points=points)
    return None
