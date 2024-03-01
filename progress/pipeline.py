from progress.logger import logging
from progress.utils import Config
from progress.entity import BOT_TOKEN_ENVIR_KEY
from progress.progress_bot.response import Response
from progress.progress_bot.bot import *


class Pipeline:
    def __init__(self):
        logging.info('Initializing Pipeline')
        self.config = Config()
        self.responses = Response(self.config.response_path)
        self.telegram_bot_token = os.environ.get(BOT_TOKEN_ENVIR_KEY)
        


    def initialize_bot(self):
        self.bot = Bot(self.config, self.responses)

        
    def run_bot(self):

        self.application = ApplicationBuilder().token(self.telegram_bot_token).build()


        start_handler = CommandHandler('start', self.bot.start)
        help_handler = CommandHandler('help', self.bot.get_help)
        get_st = CommandHandler('stat', self.bot.get_status)
        stop_handler = CommandHandler('stop', self.bot.stop)
        set_handler = CommandHandler('set', self.bot.set_value)
        get_handler = CommandHandler('get', self.bot.get_profile)
        load_profile = CommandHandler('load', self.bot.load_profile)
        csv_handler = MessageHandler(filters.Document.TEXT, self.bot.load_profile)
        start_job = CommandHandler('setup', self.bot.set_job)
        status_handler = CallbackQueryHandler(self.bot.button)
        unknown_handler = MessageHandler(filters.COMMAND, self.bot.unknown)

        self.application.add_handlers(
            handlers=[
                start_handler,
                help_handler,
                get_st,
                stop_handler,
                get_handler,
                set_handler,
                load_profile,
                csv_handler,
                start_job,
                status_handler,
                unknown_handler
            ]
        )


        self.application.run_polling()


    
        