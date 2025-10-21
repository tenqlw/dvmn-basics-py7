import ptbot
from pytimeparse import parse
from decouple import config


TG_TOKEN = config('TELEGRAM_TOKEN')
chat_id = config('TELEGRAM_CHAT_ID')
bot = ptbot.Bot(TG_TOKEN)


def wait(chat_id, message_id):
    message_id = bot.send_message(chat_id, 'Запускаю таймер...')
    bot.register_next_step_handler(message_id, notify_progress)

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify_progress(secs_left, chat_id, message_id, total_secs, bot):
    total_secs = parse(message_id)
    progressbar = render_progressbar(total_secs, total_secs - secs_left)
    bot.create_countdown(total_secs, notify_progress, chat_id=chat_id, message_id=message_id, total_secs=total_secs)
    bot.create_timer(total_secs, notify_progress, chat_id=chat_id, message_id=message_id)
    bot.update_message(f'Осталось секунд{secs_left}\n{render_progressbar}', chat_id=message.chat.id, message_id=message.message.id)

def main():
    bot.reply_on_message(wait)
    bot.send_message(chat_id, "Время вышло!")
    bot.run()

if __name__ == '__main__':
    main()