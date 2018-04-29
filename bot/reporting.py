from telegram.ext import ConversationHandler, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
from .utils import get_user, fallback_cb
from datetime import datetime

ASKING_FOR_REPORT = 0

def report_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler('report', start_reporting, pass_user_data=True)],
        states={
            ASKING_FOR_REPORT: [
                MessageHandler(Filters.text,  
                             parse_answer_and_ask_for_next_trackable,
                             pass_user_data=True)
            ]
        },
        fallbacks=[MessageHandler(Filters.text, fallback_cb, pass_user_data=True)]
    )

def start_reporting(bot, update, user_data):
    '''
    prints report start dialog, 
    inits the userdata so that the ask_for_next_report
    will work with the first trackable
    and prompts user for first report
    '''
    user = get_user(update)

    assert 'reports' not in user_data;  assert 'curr_index' not in user_data

    if not user.trackable_names: # empty sequences evaluate to false
        update.message.reply_text("You don't have any trackables yet. Create one by sending /add_trackable")
        return

    update.message.reply_text('Oh, great. Tell me what you\'ve done today:')

    user_data['reports'] = [ {
            'trackable' : trackable,
            'report' : None
        } 
        for trackable in user.trackable_names]
    user_data['curr_index'] = 0

    ask_for_trackable_report(
        user_data['reports'][0]['trackable'], update.message)

    return ASKING_FOR_REPORT

def ask_for_trackable_report(trackable_name, message):
    message.reply_text('How\'s {0} going?'.format(trackable_name))
    
def parse_answer_and_ask_for_next_trackable(bot, update, user_data):
    '''
    checks the user's anwser and adds it as value for
    the trackable user currently reports on

    the partial reports are stored in the user_data as a dict
    the current trackable is denoted by its index stored in user_data

    if there are other trackables to report,
    increments the current index and prompts user to report for next trackable 
    and finishes reporting otherwise
    '''
    assert 'reports' in user_data;  assert 'curr_index' in user_data
    
    report = update.message.text
    # TODO: validate input

    curr_index = user_data['curr_index']
    reports = user_data['reports']
    print('\nstart reports: ' + str(reports))

    reports[curr_index]['report'] = report

    if(curr_index < len(reports) - 1): # if not last
        ask_for_trackable_report(reports[curr_index + 1]['trackable'], update.message)
        user_data['curr_index'] += 1
        return ASKING_FOR_REPORT
    else:
        return finish_reporting_conv(update, user_data)


def finish_reporting_conv(update, user_data):
    save_report(user_data['reports'], get_user(update))
    update.message.reply_text('Nice! I\'ll take note of that.')
    clear_user_data(user_data)
    return ConversationHandler.END

def save_report(reports, user_wrapper):
    '''
    adds all acumulated reports 
    as entries to corresponding trackables
    (writes to db)
    '''
    assert reports
    assert 'trackable' in reports[0] and 'report' in reports[0]

    print('saving reports : {}'.format(reports))

    # from datetime import timedelta
    date_now = datetime.utcnow() #+ timedelta(days=2)

    for rep in reports:
        user_wrapper.get_trackable_wrapper(rep['trackable']).   \
            add_user_entry(date_now, rep['report'])

def clear_user_data(user_data):
    del user_data['reports']
    del user_data['curr_index']

    
# def _rand_starting_linkingword():
#     starting_lwords = [
#         'Say',
#         'So',
#         ''
#     ]
#     pass

# def _rand_middle_linkingword():

