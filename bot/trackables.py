from telegram.ext import ConversationHandler, CommandHandler, RegexHandler

ADD_PROP_NAME, ADD_LOWER_BOUND, ADD_UPPER_BOUND = range(3)

def add_trackable_conv():
    return ConversationHandler(
        entry_points=[CommandHandler('add_trackable', add_new, pass_user_data=True)],
        states={
            ADD_PROP_NAME: [
                RegexHandler('.+',
                             add_lower_bound,
                             pass_user_data=True),
            ],
            ADD_LOWER_BOUND: [
                RegexHandler('\\d+',
                             add_upper_bound,
                             pass_user_data=True),
            ],
            ADD_UPPER_BOUND: [
                RegexHandler('\\d+',
                             prop_added,
                             pass_user_data=True),
            ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )





