import random

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)
from environs import Env
from textwrap import dedent
from utils import get_random_question_and_answer


def start(update: Update, context: CallbackContext) -> str:
    buttons = [["Python", "Django", "General "], ["Случайный вопрос"]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=dedent(
            """\
        Привет! Я - Interview Prep Bot 👨‍💻
        Я помогу тебе подготовиться к собеседованию  
        """
        ),
        reply_markup=keyboard,
    )

    return 'SELECTING_ACTION'


def select_topic(update: Update, context: CallbackContext) -> str:
    selected_topic = update.message.text
    context.user_data['selected_topic'] = selected_topic

    ask_new_question(update, context)

    return 'SELECTING_ACTION'


def ask_new_question(update: Update, context: CallbackContext) -> None:
    selected_topic = context.user_data.get('selected_topic')
    buttons = [
        [
            InlineKeyboardButton(text="Узнать ответ", callback_data=str('ANSWER')),
        ],
    ]
    question, answer = get_random_question_and_answer(topic=selected_topic)
    context.user_data['selected_answer'] = answer
    keyboard = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text=question, reply_markup=keyboard)


def ask_random_question(update: Update, context: CallbackContext) -> str:
    topic = ["Python", "Django", "General"]
    selected_topic = random.choice(topic)
    question, answer = get_random_question_and_answer(topic=selected_topic)
    context.user_data['selected_answer'] = answer
    buttons = [
        [
            InlineKeyboardButton(text="Узнать ответ", callback_data=str('ANSWER')),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.message.chat_id, text=question, reply_markup=keyboard)

    return 'SELECTING_ACTION'


def send_answer(update: Update, context: CallbackContext) -> str:
    answer = context.user_data.get('selected_answer')
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

    return 'SELECTING_ACTION'


def stop(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('До встречи')

    return -1


def main():
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher

    root_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'SELECTING_ACTION': [
                MessageHandler(
                    Filters.regex('^Python$|^Django$|^General$'),
                    select_topic
                ),
                MessageHandler(
                    Filters.regex('^Случайный вопрос$'),
                    ask_random_question
                ),
                CallbackQueryHandler(
                    send_answer,
                    pattern='^' + str('ANSWER') + '$',
                ),
            ],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(root_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
