from random import random, randint
from typing import List

from input_check import looks_like_int, looks_like_float, looks_like_iso_date
from question import Question, QuestionType, QuestionDB



class Quizz:
    
    def __init__(self, number_of_questions=0):
        self._db: List[Question] = QuestionDB.get_questions(shuffle_db=True)
        #CODE BELOW: len(self._db) = number_of_questions if valid else all questions
        self._db = self._db[:number_of_questions if 0 < number_of_questions < len(self._db) else len(self._db)]
        self._answer = None
        self._user_exit = False
        self._actual_question: Question
        self._index = 0

    @property
    def run(self):
        return False if self._user_exit else self._index < len(self._db)

    def ask_question(self):
        if self.run:
            self._actual_question = self._db[self._index]
            print(f"\n{self._actual_question}")

    def get_answer(self):
        input_ok = False
        while not input_ok and self.run:
            match self._actual_question.type:
                case QuestionType.DATE: self._answer = input("EEEE-HH-NN formátumban add, meg a választ!\n--> ")
                case QuestionType.FLOAT: self._answer = input(f"Ha a számot megadhatod tört alakban is. pl. {round(randint(1, 100) + random(), 2)}  \n--> ")
                case QuestionType.SET: self._answer = input(f"Ha válaszokat felsorolva, vesszővel elválasztva add meg! (legalább egy vessző kell a továbblépéshez)\n--> ")
                case _: self._answer = input("--> ")
            self._user_exit = self._answer == "exit"
            input_ok = self._input_checker()

    def _input_checker(self) -> bool:
        match self._actual_question.type:
            case QuestionType.INT: return looks_like_int(self._answer)
            case QuestionType.FLOAT: return looks_like_float(self._answer)
            case QuestionType.DATE: return looks_like_iso_date(self._answer)
            case QuestionType.STRING: return len(self._answer) > 0
            case QuestionType.SET: return "," in self._answer
            case _: raise NotImplementedError(f"Unknown question type: {self._actual_question.type}")

    def evaluate_answer(self):
        if self.run:
            self._actual_question.evaluate(self._answer)
            self._index += 1  # important to change the index at the last step, and not before

    @property
    def max_points(self):
        return sum([x.max_point for x in self._db])

    @property
    def points(self):
        return sum([x.point for x in self._db])

    def show_statistics(self):
        print("Gratulálok!")
        print(f"Az elérhető {self.max_points} pontból {self.points} pontot kaptál. "
              f"\nEz egy {round((self.points / self.max_points) * 100, 2)}%-es eredmény.")
        if (bad_answers := [x for x in self._db if x.answer_was_not_correct]):
            print("Kérdések amikre rossz választ adtál:\n")
            print(*bad_answers, sep="\n")
