import telebot
from keys_token import key, TOKEN
from extensions import APIException, CurrencyConverter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['stat', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<Имя валюты>\
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список все доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступная валюта'
    for i in key.keys():
        text = '\n'.join((text, i,))#перенос строки скаждой
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удается обработать команду\n{e}')
    else:
        total_base_amount = float(total_base) * int(amount)
        text = f'Цена {amount} {quote} в {base} - {total_base_amount}'
        bot.send_message(message.chat.id, text)


bot.polling()




