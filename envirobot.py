from telegram.ext import Updater, CommandHandler
from envirophat import light, weather, motion, analog

from conf import BOT_TOKEN


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def environment(bot, update):
    output = """
Temp: {t}c
Pressure: {p}Pa
Light: {c}
""".format(
        t = round(weather.temperature(),2),
        p = round(weather.pressure(),2),
        c = light.light()
    )

    bot.send_message(
        chat_id=update.message.chat_id, text=output) 


def check_light_job(bot, job):
    if light.light() < 1000:
        print("Lights Off")
        bot.send_message(chat_id="@berlincodingevenings", text="Lights Off!")


def main():
    updater = Updater(BOT_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))

    updater.dispatcher.add_handler(CommandHandler('env', environment))

    updater.job_queue.run_repeating(check_light_job, interval=2, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
