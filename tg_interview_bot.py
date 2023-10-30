from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)
from environs import Env
from textwrap import dedent
from utils import get_random_question


def start(update: Update, context: CallbackContext) -> str:
    buttons = [["Python", "Django", "General "]]
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


def ask_new_question(update: Update, context: CallbackContext):
    selected_topic = context.user_data.get('selected_topic')
    if selected_topic:
        question = get_random_question(topic=selected_topic)
        context.bot.send_message(chat_id=update.message.chat_id, text=question)


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
            ],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(root_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
