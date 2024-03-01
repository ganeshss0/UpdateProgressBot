import asyncio
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    MenuButton,
    MenuButtonCommands,
)
from telegram.ext import ( 
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    filters, 
    MessageHandler,
    CallbackQueryHandler,
)

import datetime as dt
from progress.logger import logging
from progress.UpdateDayGood import UpdateValue, get_yesterday_date, Get_Year_Month_Filter
from progress.utils import load_dataset, Config, Validate_CSV
from progress.main import main
from progress.progress_bot.response import Response_Obj
import os




class Bot:
    """
    Telegram Bot Class

    # Parameters
    `config` : Configuration Object
    `response` : Response Object
    """
    def __init__(self, config: Config, responses: Response_Obj) -> None:

        self.responses = responses
        self.config = config



    # Start handler
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Sends Hello Message to User
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        """

        # Creating a user variable for user's information
        user = update.message.from_user
        # This create a hello message prefix
        hello_user = f'Hello {user.first_name}, '


        # Checking if the user is Super User or not.
        if update.effective_user.name == self.config.super_user:

            # Hello Message
            text = hello_user + self.responses.introduction
            # Sending Hello Message to User
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )
        else:
            # Hello Message
            text = hello_user + self.responses.non_user_introduction
            # Sending Hello Message to User
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )

    # Help Handler
    async def get_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        '''
        Sends Help Message to User.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''

        # Sending Message to user.
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.responses.help
        )




    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '''
        Sends the Invalid Command Message to User.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        # Storing User Detail in user.
        user = update.message.from_user
        
        # Sending Message to user.
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f'{user.first_name}, this is not a valid Command, Please input correct command.'
        )

        
    async def get_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '''
        Sends a Visualization to User
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        # Checking if User is super user
        if update.effective_user.name == self.config.super_user:
            # Sending a photo to user.
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=self.config.visualization_path)
        else:
            # Sending a photo to user.
            await update.message.reply_text(text=self.responses.non_user_introduction)



    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Stops the repeating messages to user.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        """

        # User Details
        user = update.message.from_user
        if update.effective_user.name == self.config.super_user:
        
            logging.info("User %s canceled the conversation.", update.effective_user.name)
            # Getting the repeating message job
            main_job = context.job_queue.get_jobs_by_name(self.config.super_user)

            # Removing Job
            for job in main_job:
                job.schedule_removal()
            # Sending Message to User
            await update.message.reply_text(
                text=f"Bye! {user.first_name}.", 
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.effective_chat.send_message(f'Bye, {user.first_name}')


    async def set_job(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '''
        Adds a repeating job to context, User get message in defined interval.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        if update.effective_user.name == self.config.super_user:
            # Adding job
            context.job_queue.run_daily(
                self.today_status,
                time=self.config.message_time,
                name=self.config.super_user,
                chat_id=update.effective_chat.id
            )
            await update.effective_chat.send_message(text='Setup Complete')
        else:
            await update.effective_chat.send_message('You are not allowed to setup')
    
    async def today_status(self, context: ContextTypes.DEFAULT_TYPE):
        '''
        Shows a keyboard to User with some numbers.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        # Number that are on keyboard
        reply_keyboard = [
            [InlineKeyboardButton('Zero', callback_data=0),
            InlineKeyboardButton('One', callback_data=1),
            InlineKeyboardButton('Two', callback_data=2)],
            [InlineKeyboardButton('Three', callback_data=3),
            InlineKeyboardButton('Four', callback_data=4),
            InlineKeyboardButton('Five', callback_data=5)]
            ]
        job = context.job
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        
        # Sendind the keyboard to user.
        await context.bot.send_message(
            chat_id=job.chat_id,
            text="What is your today's status?",
            reply_markup=reply_markup
        )

    async def load_profile(self, update: Update, context:ContextTypes.DEFAULT_TYPE):
        '''
        Replaces the existing data by data received from user.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        # Checking if user is super user.
        if update.effective_user.name == self.config.super_user:
            # User Details
            user = update.message.from_user
            # Checking if user sends a document
            if update.message.document:
                # checking if document's file name ends with '.csv'
                if update.message.document.file_name.endswith('.csv'):
                    # Getting File
                    file = await update.message.document.get_file()

                    # Saving File to Disk
                    await file.download_to_drive(self.config.dataset_path)
                    # Sending message to user
                    await update.effective_chat.send_message('File received')
                    # Loading the csv file into dataframe
                    data = load_dataset(self.config.dataset_path)
                    # Updating the visualization
                    main(data, self.config.dataset_path, self.config.visualization_path)
                else:
                    # Sending message to user
                    await update.effective_chat.send_message(f'{user.first_name}, Please upload a CSV file only.')
                
            else:
                # Sending Message to user
                await update.effective_chat.send_message(f'{user.first_name}, upload a CSV file.')
        else:
            await update.effective_chat.send_message(self.responses.non_user_introduction)


    async def get_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '''
        Sends the exists data to user.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        # User Detail
        user = update.message.from_user
        
        # Checking if user is super user
        if update.effective_user.name == self.config.super_user:
            # Chat ID of user
            chat_id = update.effective_chat.id
            # sending document to user
            await context.bot.send_document(chat_id=chat_id, document=self.config.dataset_path)
        else:
            # sending message to user
            await update.effective_chat.send_message(text=f'Hey {user.first_name}, what do you want.')



    async def set_value(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '''
        Update the a specific value in data based on input from user.
        # Parameters
        `update`: This object represent an incoming update.
        `context`: `ContextTypes.DEFAULT_TYPES
        '''
        # Checking if user is super user
        if update.effective_user.name == self.config.super_user:
            try:
                # Year Month Day
                year, month, day = context.args[0].split('-')

                # value (updated)
                value = int(context.args[-1])
                # loading data in dataframe
                data = load_dataset(self.config.dataset_path)


                # updating the data
                data = UpdateValue(data, int(year), int(month), day, value)
                # updating the visualization and saving the data to disk.
                main(data, self.config.dataset_path, self.config.visualization_path)

                # Sending message to user
                await update.effective_chat.send_message(text = 'Successfully Updated')
            except Exception as e:
                logging.error(e)
                # sending message to user
                await update.effective_chat.send_message(text='Usage /set <YYYY-M-D VALUE> \n Example: If you want to set a value of 0 on 2 March 2023 then write `/set 2023-3-2 0`')
        else:
            await update.effective_chat.send_message('After some time I will open this bot for public.')

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        

        query = update.callback_query
        # value entered by user
        value = int(query.data)

        day, month, year = get_yesterday_date()
        # loading data in dataframe
        data = load_dataset(self.config.dataset_path)
        # updating the data
        data = UpdateValue(data, year, month, day, value)

        # updating the visualization and saving the data to disk
        main(data, self.config.dataset_path, self.config.visualization_path)

        # Answer the callback
        await query.answer('Updated Succesfully')
        await query.delete_message()

    # async def del_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE)




# if __name__ == '__main__':
#     mytoken = os.environ.get('TELEGRAM_BOT_TOKEN')
#     application = ApplicationBuilder().token(mytoken).build()


#     start_handler = CommandHandler('start', start)
#     num_handler = MessageHandler(filters.Regex('^(0|1|2|3|4|5)$'), set_number)
#     get_st = CommandHandler('stat', get_status)
#     stop_handler = CommandHandler('stop', stop)
#     set_handler = CommandHandler('set', set)
#     unknown_handler = MessageHandler(filters.COMMAND, unknown)
    


#     application.add_handler(start_handler)
#     application.add_handler(get_st)
#     application.add_handler(stop_handler)
#     application.add_handler(num_handler)
#     application.add_handler(set_handler)
#     application.add_handler(unknown_handler)
    
#     application.run_polling()
