from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)
from commands import answering_machine, ask_random_question, ask_new_question, send_answer, select_topic, stop, start
from environs import Env


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
                MessageHandler(Filters.regex('^Python$|^Django$|^General$|^HR$|^Employers$|^Coding$'), select_topic),
                MessageHandler(Filters.regex('^Случайный вопрос$'), ask_random_question),
                MessageHandler(Filters.text & ~Filters.command, answering_machine),
                CallbackQueryHandler(send_answer, pattern='^ANSWER$'),
                CallbackQueryHandler(ask_new_question, pattern='^QUESTION$'),
            ],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(root_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
