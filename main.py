from quiz import Quiz


number_of_questions = 10
quiz = Quiz(number_of_questions)

while quiz.run:
    quiz.ask_question()
    quiz.get_answer()
    quiz.evaluate_answer()

quiz.show_statistics()




