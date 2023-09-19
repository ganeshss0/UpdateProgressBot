import asyncio
import telegram
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ( 
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    filters, 
    MessageHandler, 
    JobQueue,
    ConversationHandler
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


ACCESS_TOKEN = 'R36CdvV8sRX2Sr@%S^CbeiuhUBejbtn^q2Mwmo3oFbNb8wLimSZHYBBSMhCkdhyoi!AYX$JJ'
SUPER_USER = '@dopodix'
START_TEXT = 'Hello, I am a bot, Developed by https://t.me/dopodix . My task is to periodically sends messages to my Developer and based on their response update https://github.com/ganeshss0 this GitHub repository. Sorry, Currently I only respond to my Developer messages only. Thank you!'


# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to `/start` and `/help` commands and sends hello message to user."""
    chat_id = update.effective_chat.id

    if update.effective_user.name == SUPER_USER:
        context.job_queue.run_repeating(
            today_status, 
            interval=5, 
            name=SUPER_USER, 
            chat_id=chat_id
        )

    await update.message.reply_text(
        text=START_TEXT
        )


async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = str(context.args[0])
    
    if token:
        if token == ACCESS_TOKEN:
            pass

    await update.effective_message.reply_text('Usage: /config <AccessToken>')




async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Invalid Command, Please input correct command.'
    )


async def today_status(context:ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['0', '1', '2'], ['3', '4', '5']]
    job = context.job
    
    await context.bot.send_message(
        chat_id=job.chat_id, 
        text="What is your today's status?", 
        reply_markup=ReplyKeyboardMarkup(
            keyboard=reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder='Select a number:',
            resize_keyboard=True
        )
    )


async def callbacker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = float(context.args[0])
    if not -1 < status < 9:
        unknown(update, context)
        return
    await update.effective_message.reply_text('Progress Updated')
    
async def get_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text()

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels and ends the conversation."""

    logger.info("User %s canceled the conversation.", update.effective_user.name)
    main_job = context.job_queue.get_jobs_by_name(SUPER_USER)

    for job in main_job:
        job.schedule_removal()

    await update.message.reply_text(
        text="Bye! I hope we can talk again some day.", 
        reply_markup=ReplyKeyboardRemove()
    )

async def set_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_number = update.message.text
    await update.message.reply_text(f'/set {selected_number}')




if __name__ == '__main__':
    mytoken = '6427992574:AAFCT9BgJ7gsRHfAlFNoSzcr2ZmG0qG7Op0'
    application = ApplicationBuilder().token(mytoken).build()


    start_handler = CommandHandler('start', start)
    num_handler = MessageHandler(filters.Regex('^(0|1|2|3|4|5)$'), set_number)
    config_handler = CommandHandler('config', config)
    update_handler = CommandHandler('update', today_status)
    get_st = CommandHandler('stat', get_status)
    stop_handler = CommandHandler('stop', stop)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    


    application.add_handler(start_handler)
    application.add_handler(config_handler)
    application.add_handler(update_handler)
    application.add_handler(get_st)
    application.add_handler(stop_handler)
    application.add_handler(num_handler)
    application.add_handler(unknown_handler)
    # job_minute = job_queue.run_repeating(callback_minute, interval=5, first=10, name='SendDaily')
    application.run_polling()
