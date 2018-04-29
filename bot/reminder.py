from telegram.ext import CommandHandler
import time
from datetime import datetime, timedelta

dt = datetime.utcnow() + timedelta(seconds=3)
reminder_time = dt.time()

# print('now: {0}'.format(datetime.utcnow().time()))
# print('modified : {0}'.format(reminder_time))

def _test_cb(bot, update):
    bot.send_message(chat_id=382338945, text="hey you")


def enable_reminders_command():
    return CommandHandler("/enable_reminders", _enable_reminders,
                                  pass_args=True,
                                  pass_job_queue=True)
                                  #pass_chat_data=True)

def _enable_reminders(bot, args, job_queue):

    print(str(args))
    print(str(job_queue))

    job_queue.run_once(_test_cb, reminder_time)
    