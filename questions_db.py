from random import shuffle
from question import Question
import pickle
from typing import List
import input_check
import file_path


class Questions:

    def __init__(self, number_of_questions: int = 0):
        self._db: List[Question] = []
        self._create_database()
        self._set_db_length(number_of_questions)
        self.max_points = sum([x.max_point for x in self._db])
        self._index = 0

    def _create_database(self):
        self._load_db_from_file()
        shuffle(self._db)
        self._db = list(map(self._convert_to_question, self._db))
        self._db = [x for x in self._db if x]       #removes None-s from self._db, as a result of failed self._convert_to_question

    def _load_db_from_file(self):
        try:
            with open(file_path.QUIZ_DB, "rb") as f:
                self._db = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Fájl nem található: {file_path.QUIZ_DB}")


    def _convert_to_question(self, act) -> Question | None:
        if 3 <= len(act) <= 4:
            typ, qes, ans, *prec = act  # precision is optional in the list, so sometimes it is missing
            if input_check.is_question_ok(typ=typ, question=qes, answer=ans, prec=prec):
                return Question(question=qes, answer=ans, questiontype=typ, precision=prec)
        return None


    def _set_db_length(self, noq):
        self._number_of_questions = noq if 0 < noq < len(self._db) else len(self._db)
        self._db = self._db[:self._number_of_questions]

    def next(self) -> Question | None:
        try:
            self._index += 1
            return self._db[self._index - 1]
        except:
            return None

    @property
    def points(self):
        return sum([x.point for x in self._db])
