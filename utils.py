import json
import random


def get_random_question_and_answer(topic):
    with open('questions.json', 'r', encoding='utf-8') as file:
        file_content = json.load(file)

    if topic in file_content:
        topic_questions = file_content[topic]
        random_question = random.choice(topic_questions)
        return random_question["text"], random_question["answer"], random_question["example"]
    else:
        return None
