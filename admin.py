"""
Here you can list, create and delete questions.
"""

import file_handler
from prettytable import PrettyTable


my_questions = file_handler.load_questions(shuffle_db=False)

def list_questions():
    t = PrettyTable(['Index', 'Type', 'Question', 'Answer', 'Points', 'Precision'])
    for index, q in enumerate(my_questions, 10):
        t.add_row([index, q.type.name, q.question, q.correct_answer, q.max_point, q.precision.name])
    t.align = "l"
    print(t)

def create_question():
    print("creating")

def delete_question():
    print("deleting")


while True:
    user_input = input("1. List questions\n2. Create question\n3. Delete question\n4. Exit\n-->")
    match user_input:
        case "1": list_questions()
        case "2": create_question()
        case "3": delete_question()
        case "4": break
