# from plyer import notification
# import tkinter as tk
# from tkinter.simpledialog import askinteger
# import easygui as eg

# # Create a function to handle the notification click
# def on_notification_click(sender):
#     # Open a dialog box to enter a number
#     root = tk.Tk()
#     root.withdraw()  # Hide the root window
#     number = askinteger("Enter a Number", "Please enter a number:")
#     if number is not None:
#         notification.title = "Number Entered"
#         notification.message = f"You entered: {number}"
#         notification.notify()

# # Define notification parameters
# notification_title = "Click to Enter a Number"
# notification_message = "Click here to enter a number."

# # Create a notification
# # notification.notify(
# #     title=notification_title,
# #     message=notification_message,
# #     app_name="My App",
# #     timeout=10,  # The notification will disappear after 10 seconds
# #     # toast=on_notification_click  # Set the click handler
# #     toast=True,
# #     on_click=on_notification_click
# # )




# ############################################33


# # Create a function to handle the notification
# def show_notification():
#     notification.notify(
#         title=notification_title,
#         message=notification_message,
#         app_name="My App",
#         timeout=10  # The notification will disappear after 10 seconds
#     )

# # Create a function to open a dialog box for number entry
# def enter_number():
#     number = eg.integerbox("Please enter a number:", "Enter a Number")
#     if number is not None:
#         notification_title = "Number Entered"
#         notification_message = f"You entered: {number}"
#         show_notification()

# # Display the initial notification
# show_notification()

# # Continuously check for notification click
# while True:
#     eg.msgbox("Click OK to enter a number.")
#     enter_number()





from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Define the states for the conversation
SELECT_NUMBER = 0

def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [KeyboardButton("0"), KeyboardButton("1"), KeyboardButton("2")],
        [KeyboardButton("3"), KeyboardButton("4"), KeyboardButton("5")],
        [KeyboardButton("6"), KeyboardButton("7"), KeyboardButton("8")],
        [KeyboardButton("9")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Select a number:", reply_markup=reply_markup)

    return SELECT_NUMBER

def set_number(update: Update, context: CallbackContext) -> int:
    selected_number = update.message.text
    update.message.reply_text(f"/set {selected_number}")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

def main():
    # Create an Updater with your bot's token
    
    updater = Updater(token='6427992574:AAFCT9BgJ7gsRHfAlFNoSzcr2ZmG0qG7Op0', use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Define a conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_NUMBER: [MessageHandler(filters.regex(r'^[0-9]$'), set_number)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Register the conversation handler
    dp.add_handler(conversation_handler)
    
    # Start the bot
    updater.start_polling()
    
    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == "__main__":
    main()
