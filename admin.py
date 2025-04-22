"""
Here you can list, create and delete questions.
"""

import pickle

from prettytable import PrettyTable

from config import QUIZ_DB
from question import load_questions


my_questions = None


def _lazy_load_questions():
    global my_questions
    if not my_questions:
        my_questions = load_questions(shuffle_db=False)

def list_questions():
    _lazy_load_questions()
    global my_questions

    table = PrettyTable(['Index', 'Type', 'Question', 'Answer', 'Points', 'Precision'])
    for index, q in enumerate(my_questions, 10): #q is a Question instance
        table.add_row([index, q.type.name, q.question, q.correct_answer, q.max_point, q.precision.name])
    table.align = "l"
    print(table)

def create_question():
    print("creating")

def delete_question():
    list_questions()
    global my_questions
    try:
        index = int(input("Melyik kérdést töröljem? (index számot add meg)\n--> ")) - 10  #10 is the first index
        my_questions.pop(index if 0 <= index else len(my_questions))    #if index is negative, Python would accept it, so i set it to a not real index
        _save_questions()
        print("Sikeres törlés")
    except IndexError:
        print(f"Nem található ilyen index: {user_input}")
    except ValueError:
        print("Nem számot adott meg")

def _save_questions():
    output = [x._get_db_format() for x in my_questions]
    with open(QUIZ_DB, "wb") as f:
        pickle.dump(output, f)



run = True
while run:
    user_input = input("1. List questions\n2. Create question\n3. Delete question\n4. Exit\n-->")
    match user_input:
        case "1": list_questions()
        case "2": create_question()
        case "3": delete_question()
        case "4": run = False
