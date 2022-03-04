
import telebot
from telebot import types
from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert
cg = CoinGeckoAPI()

bot = telebot.TeleBot('5190482385:AAH-aN6jldDk0NqtzvKuTnp_-BuAohtY5Hk')


@bot.message_handler(commands=['start'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Курс крипты'), types.KeyboardButton('Конвертер'))
    cr = bot.send_message(message.chat.id, 'Мы на главной', reply_markup=b1)
    bot.register_next_step_handler(cr, step)

def step(message):
    if message.text == 'Курс крипты':
        step2(message)
    elif message.text == 'Курс фиата':
        fiat(message)
    elif message.text == 'Конвертер':
        convert1(message)

def convert1(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Bitcoin'), types.KeyboardButton('Ethereum'), types.KeyboardButton('Solana'),
           types.KeyboardButton('Polygon'), types.KeyboardButton('Binance USD'), types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, 'Выберите криптовалюту', reply_markup=b1)
    bot.register_next_step_handler(msg, convert2)

def convert2(message):
    if message.text == 'Bitcoin':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать BTC?')
        bot.register_next_step_handler(msg, bbtc)
    elif message.text == 'Ethereum':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать ETH?')
        bot.register_next_step_handler(msg, eeth)
    elif message.text == 'Solana':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать SOL?')
        bot.register_next_step_handler(msg, lltc)
    elif message.text == 'Polygon':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать MATIC?')
        bot.register_next_step_handler(msg, mmatic)
    elif message.text == 'Binance USD':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать BUSD?')
        bot.register_next_step_handler(msg, uuni)
    elif message.text == 'Назад':
        main(message)

def bbtc(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BTC == {price["bitcoin"]["usd"] * convert2} $')
    main(message)

def eeth(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='ethereum', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} ETH == {price["ethereum"]["usd"] * convert2} $')
    main(message)

def lltc(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='solana', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} SOL == {price["solana"]["usd"] * convert2} $')
    main(message)

def mmatic(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='matic-network', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} MATIC == {price["matic-network"]["usd"] * convert2} $')
    main(message)

def uuni(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='binance-usd', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BUSD == {price["binance-usd"]["usd"] * convert2} $')
    main(message)

def fiat(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('USD'), types.KeyboardButton('RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс фиата', reply_markup=b1)
    bot.register_next_step_handler(q, fiat_step2)
    main(message)

def fiat_step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Назад'))
    if message.text == 'USD':
        price = convert(base='USD', amount=1, to=['RUB', 'EUR', 'UAH', 'KZT'])
        bot.send_message(message.chat.id, f'1 USD == {price["RUB"]} RUB\n'
                                          f'1 USD == {price["EUR"]} EUR\n'
                         f'1 USD == {price["UAH"]} UAH\n'
                         f'1 USD == {price["KZT"]} KZT')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)
    if message.text == 'RUB':
        price = convert(base='RUB', amount=1, to=['USD', 'EUR', 'UAH', 'KZT'])
        bot.send_message(message.chat.id, f'1 RUB == {price["USD"]} USD\n'
                                              f'1 RUB == {price["EUR"]} EUR\n'
                                              f'1 RUB == {price["UAH"]} UAH\n'
                                              f'1 RUB == {price["KZT"]} KZT')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)
    if message.text == 'Главная':
        main(message)

def step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Курс к USD'), types.KeyboardButton('Курс к RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс моих токенов', reply_markup=b1)
    bot.register_next_step_handler(q, step3)

def step3(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Назад'))
    if message.text == 'Курс к USD':
        price = cg.get_price(ids='bitcoin, ethereum, solana, matic-network, binance-usd', vs_currencies='usd')
        bot.send_message(message.chat.id, f'Мои токены:\n\n'
                                          f'Bitcoin == {price["bitcoin"]["usd"]} $\n'
                                          f'Ethereum == {price["ethereum"]["usd"]} $\n'
                                          f'Solana == {price["solana"]["usd"]} $\n'
                                          f'Polygon == {price["matic-network"]["usd"]} $\n'
                                          f'Binance-USD == {price["binance-usd"]["usd"]} $', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == 'Курс к RUB':
        price = cg.get_price(ids='bitcoin, ethereum, solana, matic-network, binance-usd', vs_currencies='rub')
        bot.send_message(message.chat.id, f'Мои токены:\n\n'
                                              f'Bitcoin == {price["bitcoin"]["rub"]} ₽\n'
                                              f'Ethereum == {price["ethereum"]["rub"]} ₽\n'
                                              f'Solana == {price["solana"]["rub"]} ₽\n'
                                              f'Polygon == {price["matic-network"]["rub"]} ₽\n'
                                              f'Binance USD == {price["binance-usd"]["rub"]} ₽', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)
    elif message.text == 'Главная':
        main(message)
bot.polling(none_stop=True, interval=0)