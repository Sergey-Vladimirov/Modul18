import telebot


from extensions import API_Exception, Converter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту нужно перевести> \n\
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values \nУвидеть список доступных возможностей можно при помощи комманд /help и /start'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values']) #список валют
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise API_Exception('Неверный формат ввода (слишком много значений)')

        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)

    except API_Exception as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Converter as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} равен {total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()