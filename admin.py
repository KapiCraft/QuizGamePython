"""
Here you can list, create and delete questions.
"""

from prettytable import PrettyTable

from question import QuestionDB


my_questions = None


def _lazy_load_questions():
    global my_questions
    if not my_questions:
        my_questions = QuestionDB.get_questions(shuffle_db=False)

def list_questions() -> None:
    """
    Lists the questions, starting index is 10, to avoid user accidentally deleting/creating a question
    :return: None
    """
    _lazy_load_questions()
    table = PrettyTable(['Index', 'Type', 'Question', 'Answer', 'Points', 'Precision'])
    for index, q in enumerate(my_questions, 10): #q is a Question instance
        table.add_row([index, q.type.name, q.question, q.correct_answer, q.max_point, q.precision.name])
    table.align = "l"
    print(table)

def create_question():
    pass

def delete_question():
    """
    Lists the questions, then you can choose an index to delete, starting index is 10,
    to avoid user accidentally deleting a question.
    If the index provided is ok, the question will be deleted.
    :return: None
    """
    global my_questions
    list_questions()
    try:
        user_input = int(input("Melyik kérdést töröljem? (index számot add meg)\n--> "))
        index = user_input - 10 #10 is the first index
        if _is_question_index_valid(index):
            my_questions.pop(index)
            _save_questions()
            print("Sikeres törlés")
        else:
            print(f"Nem található ilyen index: {user_input}")
    except ValueError:
        print("Nem számot adott meg")

def _is_question_index_valid(index: int) -> bool:
    global my_questions
    return 0 <= index < len(my_questions)

def _save_questions():
    global my_questions
    QuestionDB.save_questions(my_questions)


run = True
while run:
    user_input = input("1. List questions\n2. Create question\n3. Delete question\n4. Exit\n-->")
    match user_input:
        case "1": list_questions()
        case "2": create_question()
        case "3": delete_question()
        case "4": run = False
