from datetime import date
from difflib import SequenceMatcher
import pickle
from random import shuffle
from typing import List

from config import QUIZ_DB
from input_check import looks_like_int, looks_like_question
from question_enums import QuestionType, Precision


class Question:
    def __init__(self, questiontype: QuestionType, question: str, answer: any,
                 points: int = 10, precision: Precision = Precision.NORMAL):
        self.type = questiontype
        self.question = question
        self._answer = None
        self.correct_answer = answer
        self.precision = precision if precision else Precision.NORMAL
        self.max_point = int(points if points else 10)
        self.point = 0

    def __repr__(self):
        return f"{self.question}"

    def evaluate(self, answer):
        self._answer = answer
        match self.type:
            case QuestionType.INT: self._evaluate_number()
            case QuestionType.FLOAT: self._evaluate_number()
            case QuestionType.DATE: self._evaluate_date()
            case QuestionType.STRING: self._evaluate_string()
            case QuestionType.SET: self._evaluate_set()
            case _: raise NotImplementedError(f"Unknown question type: {self.type}")

    def _evaluate_string(self):
        accuracy = 1 - SequenceMatcher(None, self._answer.lower(), self.correct_answer.lower()).ratio()
        self._calculate_points(accuracy)

    def _evaluate_date(self):
        d1 = date.fromisoformat(self._answer)
        d2 = date.fromisoformat(self.correct_answer)
        days = abs((d1 - d2).days)
        accuracy = 0.05 if days <= 30 else 0.1 if days <= 180 else 0.2 if days <= 365 else 1
        self._calculate_points(accuracy)

    def _evaluate_number(self):
        difference = abs(float(self.correct_answer) - float(self._answer))
        accuracy = difference / self.correct_answer
        self._calculate_points(accuracy)

    def _calculate_points(self, accuracy):
        threshold = self._get_precision_threshold()
        pts = []
        for i in threshold:
            if accuracy <= i["error_limit"]:
                pts.append(self.max_point * i["pts_multiplier"])
        self.points = round(max(pts)) if pts else 0

    def _get_precision_threshold(self) -> List[dict[str, float | int]]:
        thresholds = {
            Precision.LOW: [{"error_limit": 0.2, "pts_multiplier": 1}, {"error_limit": 0.3, "pts_multiplier": 0.8}],
            Precision.NORMAL: [{"error_limit": 0.1, "pts_multiplier": 1}, {"error_limit": 0.2, "pts_multiplier": 0.8}],
            Precision.HIGH: [{"error_limit": 0.05, "pts_multiplier": 1}, {"error_limit": 0.1, "pts_multiplier": 0.8}],
        }
        threshold = thresholds.get(self.precision, None)
        if not threshold:
            raise NotImplementedError(f"Unknown precision: {self.precision}")
        return threshold


    def _evaluate_set(self):
        self._answer = self._answer.strip().lower()
        self._answer = self._answer.split(",")
        self._answer = list(map(lambda x: x.replace("  ", " ").lstrip().rstrip(), self._answer))
        self._calculate_set_points()

    def _calculate_set_points(self):
        good_answers = [x for x in self.correct_answer if x.lower() in self._answer]
        self.point = round((len(good_answers) / len(self.correct_answer)) * self.max_point)

    @property
    def answer_was_not_correct(self):
        return self.point < self.max_point * 0.8

    def _get_db_format(self):
        return (self.type, self.question, self.correct_answer, self.max_point, self.precision)



def load_questions(shuffle_db: bool = True) -> List[Question]:
    try:
        with open(QUIZ_DB, "rb") as f:
            db = pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fájl nem található: {QUIZ_DB}")

    if shuffle_db:
        shuffle(db)
    return [x for x in list(map(_create_question, db)) if x]    #removes None-s from db, as
                                                                # a result of failed _create_question()


def _create_question(act: tuple) -> Question | None:
    if 3 <= len(act) <= 5:
        typ, question, answer, *rest = act
        precision, points = None, None
        for i in rest:
            if isinstance(i, Precision):
                precision = i
            elif looks_like_int(i):
                points = i
        if looks_like_question(typ=typ, question=question, answer=answer, precision=precision, points=points):
            return Question(question=question, answer=answer, questiontype=typ, precision=precision, points=points)
    return None
