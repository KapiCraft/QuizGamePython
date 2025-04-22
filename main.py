from quiz import Quizz


number_of_questions = 1
quiz = Quizz(number_of_questions)

while quiz.run:
    quiz.ask_question()
    quiz.get_answer()
    quiz.evaluate_answer()

quiz.show_statistics()




