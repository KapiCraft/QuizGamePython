from quiz import Quizz

quiz = Quizz(5)


while quiz.run:
    quiz.ask_question()
    quiz.get_answer()
    quiz.evaluate_answer()

quiz.show_statistics()




