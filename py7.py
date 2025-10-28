import ptbot


from pytimeparse import parse
from decouple import config


TG_TOKEN = config('TELEGRAM_TOKEN')
TG_CHAT_ID = config('TELEGRAM_CHAT_ID')
bot = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, total_secs, bot):
    progressbar = render_progressbar(total_secs, total_secs - secs_left)
    bot.update_message(chat_id, message_id, f"Осталось секунд: {secs_left}\n{progressbar}")


def last_message(bot, chat_id):
    bot.send_message(chat_id, 'Время вышло!')


def wait(chat_id, msg, bot=bot):
    seconds = parse(msg)
    if not seconds:
        bot.send_message(chat_id, 'Неверный формат времени')
        return
    message_id = bot.send_message(chat_id, f'Таймер запущен на {seconds} секунд')
    bot.create_countdown(seconds, notify_progress, chat_id=chat_id, message_id=message_id, total_secs=seconds, bot=bot)
    bot.create_timer(seconds, last_message, chat_id=chat_id, bot=bot)


def main(bot):
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == '__main__':
    main(bot)