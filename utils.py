import json
import random


def get_random_question_and_answer(topic):
    with open('questions/questions.json', 'r', encoding='utf-8') as file:
        file_content = json.load(file)

    if topic in file_content:
        topic_questions = file_content[topic]
        random_question = random.choice(topic_questions)
        return random_question["text"], random_question["answer"], random_question["example"]
    else:
        return None


def get_next_question_and_answer(topic, context):
    with open('questions/questions.json', 'r', encoding='utf-8') as file:
        file_content = json.load(file)

    if topic in file_content:
        topic_questions = file_content[topic]
        current_question_index = context.user_data.get('current_question_index', 0)
        if current_question_index < len(topic_questions):
            context.user_data['current_question_index'] = current_question_index + 1
            return (
                topic_questions[current_question_index]["text"],
                topic_questions[current_question_index]["answer"],
                topic_questions[current_question_index]["example"]
            )
    return None
