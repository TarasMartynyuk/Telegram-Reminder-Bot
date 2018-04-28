import re
from datetime import datetime, timedelta
from .utils import get_user

#region show stats
def trackable_and_date_tokens(tokens):
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

def date_back(number_of, time_unit):
    if time_unit == 'week':
        return datetime.now() - timedelta(weeks=int(number_of)), number_of * 7
    if time_unit == 'day':
        return datetime.now() - timedelta(days=int(number_of)), number_of
    if time_unit == 'month':
        return datetime.now() - timedelta(months=int(number_of)), number_of * 30
    if time_unit == 'year':
        return datetime.now() - timedelta(months=12 * int( number_of)), number_of * 365
    raise KeyError('{} is not day, week, etc.'.format(time_unit))

def show_stats(bot, update, user_data, req):
    print ("show stats ")
#     update.message.reply_text("Stats: from {} to {}".format(req['from'], req['to']))
#     update.message.reply_text([d['value'] for d in get_n_last_entries(user_id_from_update(update), req['trackable'], int(req['entry_n']))])
    # save_stats_img([entry['val'] for entry in get_n_last_entries(user_id_from_update(update), req['trackable'], req['entry_n'])])
    # bot.send_photo(chat_id=update.message.chat.id, photo=open(stat_img_filename, 'rb'))

def show_stats_request(bot, update, user_data):
    '''
    usage: /stats trackable_name number_of time_units
    '''
    # write what statistics he wants to see
    # ask time range
    # or show it for one week and ask if he wants to change the range
    # or maybe let statistics be a command
    # /stats learning 1 week
    # /stats learning 1 month
    # /stats learning 1 day
    # /stats learning 1 year
    # this means he must type trackable name
    # /trackables lists all trackables he has
    # /add_trackable start conversation about his new trackable
    # /report
    # /help write some basic tutorial-like stuff

    tokens = update.message.text.split()
    if len(tokens) == 1:
        # no args, ignore or sth
        update.message.reply_text("usage: /stats trackable_name number_of time_units")
    else:
        mb_trackable_tokens, date_tokens = trackable_and_date_tokens(tokens)
        mb_trackable = ' '.join(mb_trackable_tokens)

        if mb_trackable in get_user(update).trackable_names: # TODO:
            start_date, days_num = date_back(date_tokens[0], date_tokens[1])
            stats_request = {
                "trackable": mb_trackable,
                "from": start_date,
                "to": datetime.now(),
                "entry_n": days_num
            }
            show_stats(bot, update, user_data, stats_request)
        else:
            update.message.reply_text("there is no trackable {}".format(mb_trackable))

# def save_stats_img(nums):
#     matplotlib.style.use('seaborn')
#     plt.plot(range(len(nums)), nums)
#     plt.gcf().savefig(stat_img_filename)
#endregion




    # show_stats_conversation = ConversationHandler(
    #     entry_points=[CommandHandler('stats', show_stats_request, pass_user_data=True)],
    #     states={

    #     },
    #     fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    # )
    # dp.add_handler(show_stats_conversation)

    # dp.add_handler(CommandHandler('stats', show_stats_request, pass_user_data=True))




