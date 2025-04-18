from questions_db import Questions
from question import Question
from question_type import QuestionType
import input_check
from random import random, randint


class Quizz:

    def __init__(self, number_of_questions=0):
        self._questions = Questions(number_of_questions)
        self._answer = None
        self._user_exit = False
        self._actual_question: Question = True

    @property
    def run(self):
        return False if self._user_exit else self._actual_question

    def ask_question(self):
        self._actual_question = self._questions.next()
        if self._actual_question:
            print(f"\n{self._actual_question}")

    def get_answer(self):
        if self.run:
            input_ok = False
            while not input_ok:
                match self._actual_question.type:
                    case QuestionType.DATE: self._answer = input("EEEE-HH-NN formátumban add, meg a választ!\n--> ")
                    case QuestionType.FLOAT: self._answer = input(f"Ha a számot megadhatod tört alakban is. pl. {round(randint(1, 100) + random(), 2)}  \n--> ")
                    case _: self._answer = input("--> ")
                self._user_exit = self._answer == "exit"
                input_ok = self._input_checker()

    def _input_checker(self) -> bool:
        match self._actual_question.type:
            case QuestionType.INT: return input_check.is_int_like(self._answer)
            case QuestionType.FLOAT: return input_check.is_float_like(self._answer)
            case QuestionType.DATE: return input_check.is_iso_date_like(self._answer)
            case QuestionType.STRING: return len(self._answer) > 0
            case _: return True

    def evaluate_answer(self):
        if self.run:
            self._actual_question.evaluate(self._answer)


    @property
    def max_points(self):
        return self._questions.max_points

    @property
    def points(self):
        return self._questions.points
    @property
    def number_of_questions(self):
        return self._questions._number_of_questions

    def show_statistics(self):
        print("Gratulálok!")
        print(f"Az elérhető {self.max_points} pontból {self.points} pontot kaptál. "
              f"\nEz egy {round((self.points / self.max_points) * 100, 2)}%-es eredmény.")
        print("Kérdések amikre nem jó választ adtál:\n")
        print(*[x for x in self._questions._db if x.answer_was_not_correct], sep="\n")
