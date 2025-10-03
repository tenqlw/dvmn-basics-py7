import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') 

bot = ptbot.Bot(TG_TOKEN)

def wait(chat_id, message):
    message_id = bot.send_message(chat_id, 'Запускаю таймер...')

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify_progress(secs_left, chat_id, message_id, total_secs):
    total_secs = parse(message_id)
    progressbar = render_progressbar(total_secs, total_secs - secs_left)
    bot.create_countdown(total_secs, notify_progress, chat_id=chat_id, message_id=message_id, total_secs=total_secs)
    bot.create_timer(total_secs, notify_progress, chat_id=chat_id, message_id=message_id)
    bot.update_message(chat_id, message_id, f'Осталось секунд{secs_left}\n{render_progressbar}')

def main(chat_id, message_id):
    bot.update_message(chat_id, 'Время вышло')

if __name__ == '__main__':
    bot.reply_on_message(wait);

    bot.run()
