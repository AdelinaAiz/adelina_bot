# Создание Telegram Bot - знакомство со мной
import config
import db_state
import telebot
import random
from telebot import types

bot = telebot.TeleBot('6574375480:AAFDzPR6245hCD7zY9B-OTReCmf_fLKcvBU')


@bot.message_handler(commands=['start'])
def welcome(message):
    # Приветствие
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} 👋!\n'
                                      'Меня зовут Аделина 😃.\n' +
                     'Благодаря этому боту, вы можете познакомиться со мной поближе ❤️.')

    # Кнопочное меню
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_look = types.KeyboardButton('Посмотреть 👀')
    button_read = types.KeyboardButton('Почитать 📖')
    button_listen = types.KeyboardButton('Послушать 🎧')
    button_link = types.KeyboardButton('Ссылка ✅')
    button_advice = types.KeyboardButton('Совет 🤓')
    keyboard.add(button_look, button_read, button_listen, button_link, button_advice)

    # Инструкция
    bot.send_message(message.chat.id, "Для удобства внизу расположены кнопки (а также команды):\n"
                                      "1) /lookphoto - Посмотреть мои фотографии.\n"
                                      "2) /readpost - Почитать пост о моем главном увлечении.\n"
                                      "3) /listenstory - Послушать мои аудио ответы.\n"
                                      "4) /getlink - Получить ссылку на публичный репозиторий\n"
                                      "5) /advice - Получить случайный совет",
                     reply_markup=keyboard)
    db_state.set_state(message.chat.id, config.States.s_all.value)  # Устанавливает начальное состояние диалога



@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Посмотреть 👀' or message.text == '/lookphoto':
            # Можно реакцию на /lookphoto прописать отдельно
            markup_inline = types.InlineKeyboardMarkup()
            photo1 = types.InlineKeyboardButton(text='1 фото', callback_data='photo_1')
            photo2 = types.InlineKeyboardButton(text='2 фото', callback_data='photo_2')
            markup_inline.add(photo1, photo2)
            bot.send_message(message.chat.id, 'Что выберешь?\n'
                                              '1) Крайнее селфи\n'
                                              '2) Фото из старшей школы',
                             reply_markup=markup_inline)
        elif message.text == 'Почитать 📖' or message.text == '/readpost':
            bot.send_message(message.chat.id, 'Мое главное хобби: роспись одежды 🎨.\n\n'
                                              'Я всегда любила рисовать. Поэтому в детстве меня отдали в художественную'
                                              ' школу.\nУчилась я на отлично, поэтому все знакомые пророчили мне '
                                              'карьеру дизайнера, художника, архитектора.\n\nНо буквально за несколько '
                                              'месяцев до ЕГЭ я открыла для себя программирование. '
                                              'Очнулась уже, когда подала свои документы в университет на специальность'
                                              ' \"Прикладная математика и информатика\". Но данный факт не мешает '
                                              'мне периодически брать в руки кисть и рисовать что-нибудь новенькое'
                                              '😉.')
            bot.send_photo(message.chat.id, photo=open('media/images/drawing.JPG', 'rb'))
        elif message.text == 'Послушать 🎧' or message.text == '/listenstory':
            bot.send_message(message.chat.id, "Напиши, что бы ты хотел(а) послушать:\n\n"
                                              "1) Что такое GPT простыми словами.\n"
                                              "2) Разница между SQL и noSQL.\n"
                                              "3) История моей первой любви (Все события и герои вымышлены. "
                                              "Любые совпадения с реальными личностями случайны.)\n\n"
                                              "Пример запроса: \"Хочу послушать про sql\"\n"
                                              "Ключевые слова: GPT, SQL, любовь.")
            db_state.set_state(message.chat.id, config.States.s_listen.value)  # Смена состояния диалога
        elif message.text == 'Ссылка ✅' or message.text == '/getlink':
            bot.send_message(message.chat.id, 'Ссылка на исходный код моего бота: https://ya.ru/')
        elif message.text == 'Совет 🤓' or message.text == '/advice':
            bot.send_photo(message.chat.id, photo=open(f'media/images/{random.randint(1, 5)}.JPG', 'rb'))
        else:  # Сообщение от пользователя(не кнопка)
            if db_state.get_state(message.chat.id) == config.States.s_listen.value:
                stories = dict(gpt=lambda x: open('media/audio/GPT.mp3', 'rb'),
                               sql=lambda x: open('media/audio/SQL.mp3', 'rb'),
                               любовь=lambda x: open('media/audio/LOVE.mp3', 'rb'))
                for key, value in stories.items():
                    if key in message.text.lower():
                        audio = stories[key](message)
                        bot.send_audio(message.chat.id, audio)
                        break
                else:
                    bot.send_message(message.chat.id, 'Что-то не так. Попробуй написать снова.')
            else:
                bot.send_message(message.chat.id, 'Что-то не так. Если хочешь послушать историю,'
                                                  ' то нажми кнопку \"Послушать 🎧\"')

@bot.callback_query_handler(func=lambda call: True)
def view_photo(call):
    if call.data == 'photo_1':
        bot.send_photo(call.message.chat.id, photo=open("media/images/photo_1.jpg", 'rb'))
    elif call.data == 'photo_2':
        bot.send_photo(call.message.chat.id, photo=open("media/images/photo_2.jpg", 'rb'))


bot.polling(none_stop=True)
