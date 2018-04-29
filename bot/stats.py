import re
from datetime import datetime, timedelta
from .utils import get_user, fallback_cb
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler

filename_pr = 'chart'
ext = '.png'

def _chart_filename_for_user(username, id):
    return '{0}_{1}_{2}{3}'.format(filename_pr, username, id, ext) 

def stats_conversation():
    return CommandHandler('stats', _show_stats_request, pass_user_data=True)

def _show_stats_table(update, req):
    print ("show stats ")
    update.message.reply_text("Stats: from {} to {}".format(req['from'], req['to']))

    trackable = get_user(update).get_trackable_wrapper(req['trackable'])
    update.message.reply_text([d['value'] for d in trackable.get_user_entries(int(req['entry_n']))])

def _show_chart(entries, start_date, end_date):
    '''
    start_date and end_date are of type datetime.date
    '''

    print(str(entries))
    pass

def _show_stats_request(bot, update, user_data):
    '''
    usage: /stats trackable_name number_of time_units
    '''
    tokens = update.message.text.split()

    # print('tokens: ' + str(tokens))
    if len(tokens) == 1:
        update.message.reply_text("usage: /stats trackable_name number_of time_units")
    else:
        mb_trackable_tokens, date_tokens = _trackable_and_date_tokens(tokens)
        mb_trackable = ' '.join(mb_trackable_tokens)

        user = get_user(update)


        if user.trackable_registered(mb_trackable):
            start_date = _start_date_from_user_input(date_tokens[0], date_tokens[1])

            entries_with_missing = user.get_trackable_wrapper(mb_trackable).\
                get_entries_for_period(start_date, datetime.utcnow())

            _show_chart(_pick_values_fill_missing(entries_with_missing), 
                start_date.date(), datetime.utcnow())
        else:
            update.message.reply_text("there is no trackable {}".format(mb_trackable))

#region helpers

def _pick_values_fill_missing(entries):
    '''
    entries is a list of {
        date : datetime,
        value : int
    }
    returns a list of values - one for each day between the smallest
    and the largest datetime in entries
    values for missing days will be present as zeroes
    '''

    assert entries

    print(str(entries))

    start_date = entries[0]['date'].date()
    end_date = entries[len(entries) -1]['date'].date()

    days = (end_date - start_date).days
    print('days: ' + str(days))

    period_vals = []
    entry_index = 0
    curr_day_date = start_date

    for i in range(days + 1):
        assert entry_index < len(entries)

        print('iter : {}, entries date: {},\ncurr_day_date : {}'.format(
            i, entries[entry_index]['date'].date(), curr_day_date))

        if entries[entry_index]['date'].date() == curr_day_date:
            period_vals.append(entries[entry_index]['value'])
            entry_index += 1
        else:
            period_vals.append(0)
        
        curr_day_date += timedelta(days=1)

    return period_vals


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

def _start_date_from_user_input(number_of, time_unit):
    '''
    calculates the start date for the user requested period of time
    that period goes backwards from now(week ago etc)

    returned obj is of type datetime
    '''
    if time_unit == 'week':
        return datetime.now() - timedelta(weeks=int(number_of))
    if time_unit == 'day':
        return datetime.now() - timedelta(days=int(number_of))
    if time_unit == 'month':
        return datetime.now() - timedelta(days=int(number_of) * 30)
    # if time_unit == 'year':
        # return datetime.now() - timedelta(months=12 * int( number_of))
    raise KeyError('{} is not day, week, etc.'.format(time_unit))



#endregion