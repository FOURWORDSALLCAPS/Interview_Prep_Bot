import random

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
)
from textwrap import dedent
from question_manager import get_next_question_and_answer, get_random_question_and_answer


def start(update: Update, context: CallbackContext) -> str:
    context.user_data['current_question_index'] = 0
    context.user_data['selected_topic'] = None
    buttons = [['Python', 'Django', 'General'], ['Случайный вопрос'], ['HR', 'Employers', 'Coding']]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=dedent(
            '''\
        Привет! Я - Interview Prep Bot 👨‍💻
        Я помогу тебе подготовиться к собеседованию  
        '''
        ),
        reply_markup=keyboard,
    )

    return 'SELECTING_ACTION'


def select_topic(update: Update, context: CallbackContext) -> str:
    selected_topic = update.message.text
    previous_topic = context.user_data.get('selected_topic')

    if selected_topic != previous_topic:
        context.user_data['selected_topic'] = selected_topic
        context.user_data['current_question_index'] = 0

    return ask_new_question(update, context)


def ask_new_question(update: Update, context: CallbackContext) -> str:
    selected_topic = context.user_data.get('selected_topic')
    if selected_topic:
        question_and_answer = get_next_question_and_answer(selected_topic, context)
        if question_and_answer:
            question, answer, example = question_and_answer
            buttons = [
                [InlineKeyboardButton(text='Узнать ответ', callback_data='ANSWER')],
            ]
            keyboard = InlineKeyboardMarkup(buttons)
            context.user_data['selected_answer'] = answer
            context.user_data['selected_example'] = example
            context.bot.send_message(chat_id=update.message.chat_id, text=question, reply_markup=keyboard)
        else:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text='Вопросы по этой теме закончились.'
            )

    return 'SELECTING_ACTION'


def ask_random_question(update: Update, context: CallbackContext) -> str:
    topic = ['Python', 'Django', 'General']
    selected_topic = random.choice(topic)
    question, answer, example = get_random_question_and_answer(topic=selected_topic)
    context.user_data['selected_answer'] = answer
    context.user_data['selected_example'] = example
    buttons = [
        [
            InlineKeyboardButton(text='Узнать ответ', callback_data='ANSWER'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text=question, reply_markup=keyboard)

    return 'SELECTING_ACTION'


def send_answer(update: Update, context: CallbackContext) -> str:
    answer = context.user_data.get('selected_answer')
    example = context.user_data.get('selected_example')
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    if example != 'False':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'<code>{example}</code>',
            parse_mode=ParseMode.HTML
        )

    return 'SELECTING_ACTION'


def answering_machine(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Не совсем понял вас!')

    return 'SELECTING_ACTION'


def stop(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('До свидания! Если вы хотите начать снова, используйте /start.')

    return ConversationHandler.END
