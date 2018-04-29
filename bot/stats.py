import re
from datetime import datetime, timedelta
from .utils import get_user, fallback_cb
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler


filename_pr = 'chart'
ext = '.png'

def chart_filename_for_user(username, id):
    return '{0}_{1}_{2}{3}'.format(filename_pr, username, id, ext) 

def stats_conversation():
    return CommandHandler('stats', show_stats_request, pass_user_data=True)

def fill_missing_entries(entries):
    pass

def show_stats_table(update, req):
    print ("show stats ")
    update.message.reply_text("Stats: from {} to {}".format(req['from'], req['to']))

    trackable = get_user(update).get_trackable_wrapper(req['trackable'])
    update.message.reply_text([d['value'] for d in trackable.get_user_entries(int(req['entry_n']))])

def show_stats_request(bot, update, user_data):
    '''
    usage: /stats trackable_name number_of time_units
    '''
    tokens = update.message.text.split()

    print('tokens: ' + str(tokens))
    if len(tokens) == 1:
        # no args, ignore or sth
        update.message.reply_text("usage: /stats trackable_name number_of time_units")
    else:
        mb_trackable_tokens, date_tokens = _trackable_and_date_tokens(tokens)
        mb_trackable = ' '.join(mb_trackable_tokens)

        if get_user(update).trackable_registered(mb_trackable):
            start_date, days_num = _date_back(date_tokens[0], date_tokens[1])
            stats_request = {
                "trackable": mb_trackable,
                "from": start_date,
                "to": datetime.now(),
                "entry_n": days_num
            }
            show_stats_table(bot, stats_request)
        else:
            update.message.reply_text("there is no trackable {}".format(mb_trackable))




#region helpers

def get_entries_with_forgotten(start_date):
    '''
    returns an arr of entries corresponding for the period
    between start_date and now
    if the user did not add an entry some day, the entry with value of 0 will be there
    '''


    pass

def parse_stats_request():
    pass



def _trackable_and_date_tokens(tokens):
    if len(tokens) >= 2:
        if len(tokens) >= 4:
            mb_number_of, mb_time_units = tokens[-2:]
            if re.match(r"^[1-9]\d*$", mb_number_of) and re.match("^(week|month|day|year)$", mb_time_units):
                # last two tokens are number_of time_units, so
                return tokens[1:-2], tokens[-2:]
            else:
                return tokens[1:], ['1', 'week']
        else:
            return tokens[1:], ['1', 'week']
    else:
        return None, None

def _date_back(number_of, time_unit):
    if time_unit == 'week':
        return datetime.now() - timedelta(weeks=int(number_of)), number_of * 7
    if time_unit == 'day':
        return datetime.now() - timedelta(days=int(number_of)), number_of
    if time_unit == 'month':
        return datetime.now() - timedelta(months=int(number_of)), number_of * 30
    if time_unit == 'year':
        return datetime.now() - timedelta(months=12 * int( number_of)), number_of * 365
    raise KeyError('{} is not day, week, etc.'.format(time_unit))

def start_date_from_user_input(number_of, time_unit):
    '''
    calculates the start date for the user requested period of time
    that period goes backwards from now(week ago etc)

    returned obj is of type date
    '''
    pass

#endregion







