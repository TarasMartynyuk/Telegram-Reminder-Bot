from telegram.ext import CommandHandler

def enable_reminders_command():
    return CommandHandler("/enable_reminders", _enable_reminders,
                                  pass_args=True,
                                  pass_job_queue=True)
                                  #pass_chat_data=True)

def _enable_reminders(bot, update, args, job_queue):

    print(str(args))

    print(str(job_queue))
    pass