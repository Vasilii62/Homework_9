import telebot
from tic_tac_toe import game
import log_generate as lg
from config import TOKEN_API
from Keybords import *
from telebot import types
from time import sleep
from calc import model_racional as mr
from phonebook import working_with_datebase as wd

# Глобальные переменные и константы
bot = telebot.TeleBot(TOKEN_API)
chat_id = ''
message_id = 0
dic = {}
list_text = list()
list_callback = list()
surname = ''
name = ''
patronymic = ''
email_address = ''
telephone = ''
HELP_COMMAND = """
<b>/tic_tac_toe</b> - <i>Запускает игру Крестики-Нолики</i>
<b>/calc</b> - <i>Запускает решение примеров</i>
<b>/phonebook</b> - <i>Работа с телефонным справочником</i>
<b>/help</b> - <i>Выводит список команд с пояснениями</i>"""


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHhyhj2Q3G8_LnmlZTrKD5asKpoCTTjQACGCMAAu0HgUrqmupuzpQQ6y0E',
                     reply_markup=keyboard_start)


@bot.message_handler(commands=['help'])
def help_command(message: types.Message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_message(message.chat.id, HELP_COMMAND, parse_mode='HTML')


# Игра в крестики-нолики
@bot.message_handler(commands=['tic_tac_toe'])
def tic_tac_game(message: types.Message):  # Выбор функций бота
    global chat_id
    chat_id = message.chat.id
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHi2Jj2ov3gyGrRmMg64l3VXS6-3AKuwACUgADYIltDBp238_XJHBwLgQ')
    bot.send_message(message.chat.id, 'Давай играть! Чур у меня нолики! Хочешь ходить первым?')
    lg.write_data(f'Начинается игра "крестики-нолики"')
    global dic
    dic = {'1': '.', '2': '.', '3': '.', '4': '.', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.'}
    lg.write_data(f'Словарь заполнен пробелами')
    bot.register_next_step_handler(message, start_game)


def start_game(message):  # Функция определения, кто будет ходить первым
    global list_text, list_callback, message_id
    list_text, list_callback = get_clean_lists()  # получаем чистые листы для клавиатуры
    if message.text.lower() == 'да':
        lg.write_data(f'Пользователь принял решение ходить первым')
        message_id = bot.send_message(message.chat.id, 'Выбери клетку!',
                                      reply_markup=update_keyboard_tic_tac(list_text,list_callback)).message_id
    elif message.text.lower() == 'нет':
        lg.write_data(f'Бот ходит первым')
        bot.send_message(message.chat.id, 'Хорошо, я начинаю!')
        message_id = message.message_id
        pc_check()
    else:
        lg.write_data(f'В функции определения хода зафиксирована неизвестная команда "{message.text}"')
        bot.send_message(message.chat.id, 'Я тебя не пониманию! Скажи еще раз!')
        bot.register_next_step_handler(message, start_game)


@bot.callback_query_handler(func=lambda callback: callback.data != '_' and len(callback.data) < 2)
def user_check(callback: types.CallbackQuery):
    global list_text, list_callback, dic, message_id
    message_id = callback.message.message_id
    key = callback.data
    lg.write_data(f'Пользователь выбрал клетку {key}')
    list_text[int(key)-1] = '❌'
    list_callback[int(key)-1] = '_'
    dic[key] = 'x'
    if game.check_winner(dic):
        bot.edit_message_text('Ты выиграл!!', callback.message.chat.id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEHjfpj21nUQdP4CspZIDuDLUiXsYIuOwAClygAAhcXgEq2a7UNPA1jui4E')
        sleep(3)
        list_text, list_callback = get_clean_lists()  # получаем чистые листы для клавиатуры
        bot.delete_message(chat_id, message_id)
    elif '.' not in dic.values():
        bot.edit_message_text('У нас ничья!', callback.message.chat.id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEHjfZj21l0OmNtMUnqPym4N5ibvAOKcQACsSgAAtyCgErABNl49-Pvqy4E')
        sleep(3)
        list_text, list_callback = get_clean_lists()  # получаем чистые листы для клавиатуры
        bot.delete_message(chat_id, message_id)
    else:
        bot.edit_message_text('Я хожу!', chat_id=chat_id, message_id=message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        pc_check()


def pc_check():  # Ход бота
    global list_text, list_callback, dic, message_id
    lg.write_data(f'Начался ход бота')
    bot_choice = game.pc_choice(dic)
    lg.write_data(f'Бот выбирает клетку {bot_choice}')
    list_text[int(bot_choice)-1] = '⚪️'
    list_callback[int(bot_choice)-1] = '_'
    if 'x' not in dic.values():
        bot.send_message(chat_id, 'Твой ход!', reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        dic[bot_choice] = '0'
    else:
        dic[bot_choice] = '0'
        if game.check_winner(dic):
            lg.write_data(f'Бот победил в игре')
            bot.edit_message_text('Я победил!', chat_id, message_id,
                                  reply_markup=update_keyboard_tic_tac(list_text, list_callback))
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEHjfRj21kdEf2zMEdDxp0LHrd2xtanZgACoiwAAr7HgEpogKU2nF47iy4E')
            sleep(3)
            list_text, list_callback = get_clean_lists()  # получаем чисты листы для клавиатуры
            bot.delete_message(chat_id, message_id)
        elif '.' not in dic.values():
            lg.write_data(f'Игра завершилась ничьей')
            bot.edit_message_text('Ой у нас ничья!', chat_id, message_id,
                                  reply_markup=update_keyboard_tic_tac(list_text, list_callback))
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEHjfZj21l0OmNtMUnqPym4N5ibvAOKcQACsSgAAtyCgErABNl49-Pvqy4E')
            sleep(3)
            list_text, list_callback = get_clean_lists()  # получаем чисты листы для клавиатуры
            bot.delete_message(chat_id, message_id)
        else:
            bot.edit_message_text('Твой ход!', chat_id, message_id,
                                  reply_markup=update_keyboard_tic_tac(list_text, list_callback))


def get_clean_lists():  # чистые листы для клавиатуры
    list_t = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    list_cal = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    return list_t, list_cal


# Калькулятор
@bot.message_handler(commands=['calc'])
def calc_command(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHjotj23njbDoc0hH6f0DMmeghAQIGhwACXAADYIltDAgZgYxjUpb6LgQ')
    bot.send_message(message.chat.id, 'Вводи пример!')
    bot.register_next_step_handler(message, count_example)


def count_example(message):  # Функиця решения примера
    example, example_list = mr.get_nums(message.text)
    lg.write_data(f'Пользователь ввел пример: {example}')
    result = mr.get_result(example_list)
    lg.write_data(f'Получен ответ: {result}')
    bot.send_message(chat_id, f'{example} = {result}')


# Телефонный справочник
@bot.message_handler(commands=['phonebook'])
def phonebook_command(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Что будем делать?', reply_markup=keyboard_phonebook)


@bot.callback_query_handler(func=lambda callback: callback.data)
def user_choice(callback: types.CallbackQuery):
    choice = callback.data
    lg.write_data(f'Бот получил команду "{choice}"')
    if choice == 'Добавить контакт':
        lg.write_data(f'Начато создание контакта')
        get_name()
    elif choice == 'Найти контакт':
        lg.write_data(f'Запущен поиск контакта')
        message = bot.send_message(chat_id, 'Введите одно из данных для поиска')
        bot.register_next_step_handler(message, find_contact)
    elif choice == 'Удалить контакт':  # Удалить контакт
        lg.write_data(f'Запущено удаление контакта')
        message = bot.send_message(chat_id, 'Выбери контакт из списка и введи цифру!')
        bot.send_message(chat_id, wd.print_book())
        lg.write_data(f'Пользователю выведен справочник')
        bot.register_next_step_handler(message, del_contact)
    elif choice == 'Показать справочник':  # Вывод справочника
        lg.write_data(f'Запущен вывод справочника')
        bot.send_message(chat_id, wd.print_book())
        phonebook_command(callback.message)
    elif choice == 'Импортировать справочник':  # Импорт данных из получаемого файла
        lg.write_data(f'Запущен импорт словаря из внешнего файла')
        message = bot.send_message(chat_id, 'Отправьте мне файл .txt')
        bot.register_next_step_handler(message, import_base)
    elif choice == 'Экспортировать справочник':
        lg.write_data(f'Запущен экспорт справочника')
        message = bot.send_message(chat_id, 'В каком формате отправить справочник?\n'
                                            '1. Одна запись - на одной строке;\n'
                                            '2. Каждое значение на отдельной строке\n'
                                            'Введите цифру!')
        bot.register_next_step_handler(message, export_file)
    elif choice == 'Выход':
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEHjoRj23GFRLHXgRSs5FftXq_Mz-iBcwACbQADYIltDNNb9ft2ZA6HLgQ')
    else:
        lg.write_data(f'Зафиксирована неизвестная команда')
        mes_id_1 = bot.send_sticker(chat_id,
                                    'CAACAgIAAxkBAAEHijdj2jpoePppDQ-ye4hVXVIGBehfFAACByYAArCAgEqLpTHeB5NBWy4E').message_id
        mes_id_2 = bot.send_message(chat_id, 'Ты ввел что-то не то!').message_id
        sleep(3)
        bot.delete_message(chat_id, mes_id_1)
        bot.delete_message(chat_id, mes_id_2)


def get_name():  # Запрашиваем имя
    mess = bot.send_message(chat_id, 'Введите имя')
    bot.register_next_step_handler(mess, get_surname)


def get_surname(mess):  # Заносим в переменную имя и запрашиваем фамилию
    global name
    name = mess.text.capitalize()
    lg.write_data(f'Получено имя контакта {name}')
    bot.send_message(chat_id, 'Введите фамилию')
    bot.register_next_step_handler(mess, get_patronymic)


def get_patronymic(mess):  # Заносим в переменную фамилию и запрашиваем отчество
    global surname
    surname = mess.text.capitalize()
    lg.write_data(f'Получена фамилия контакта {surname}')
    bot.send_message(chat_id, 'Введите отчество')
    bot.register_next_step_handler(mess, get_email)


def get_email(mess):  # Заносим в переменную отчество и запрашиваем email
    global patronymic
    patronymic = mess.text.capitalize()
    lg.write_data(f'Получено отчество контакта {patronymic}')
    bot.send_message(chat_id, 'Введите email')
    bot.register_next_step_handler(mess, get_telephone)


def get_telephone(mess):  # Заносим в переменную email и запрашиваем телефон
    global email_address
    email_address = mess.text
    lg.write_data(f'Получен email контакта {email_address}')
    bot.send_message(chat_id, 'Введите телефон')
    bot.register_next_step_handler(mess, set_data)


def set_data(mess):  # Заносим в переменную телефон и записываем контакт в базу
    global telephone
    telephone = mess.text
    lg.write_data(f'Получен телефон контакта {telephone}')
    wd.add_contact(surname, name, patronymic, email_address, telephone)
    bot.send_message(chat_id, 'Контакт добавлен')
    phonebook_command(mess)


def find_contact(mess):  # Поиск контакта в справочнике
    text = mess.text
    lg.write_data(f'Для поиска от пользователя получены данные: {text}')
    text = wd.find_in_book(text)
    if text:
        lg.write_data(f'Найдены данные:\n {surname}')
        bot.send_message(chat_id, text)
        phonebook_command(mess)
    else:
        lg.write_data(f'Поиск ни чего не нашел')
        bot.send_message(chat_id, 'Ни чего не нашел')
        phonebook_command(mess)


def del_contact(message):  # Удаление контакта
    key = message.text
    if key.isdigit() and int(key) in wd.book.keys():
        lg.write_data(f'От пользователя получен ключ: {key}')
        del wd.book[int(key)]
        lg.write_data(f'Контакт удален из справочника')
        bot.send_message(chat_id, 'Контакт удален')
        phonebook_command(message)
    else:
        lg.write_data(f'От пользователя получен ключ: {key}, контакт не найден!')
        bot.send_message(chat_id, 'Контакт не найден!')
        phonebook_command(message)


def import_base(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'E:/УЧЕБА/Home_Work/phonebook/files' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    lg.write_data(f'Файл получен и сохранен')
    wd.import_base(src)
    lg.write_data(f'Импорт завершен')
    bot.send_message(chat_id, 'Импорт данных завершен!')
    phonebook_command(message)


def export_file(message):
    if message.text == '1':
        lg.write_data(f'Запущен экспорт по первому правилу')
        wd.ex_base(message.text)
        bot.send_document(chat_id, open(r'E:/УЧЕБА/Home_Work/phonebook/export.csv', 'rb'))
        phonebook_command(message)
    elif message.text == '2':
        lg.write_data(f'Запущен экспорт по второму правилу')
        wd.ex_base(message.text)
        bot.send_document(chat_id, open(r'E:/УЧЕБА/Home_Work/export_2.csv', 'rb'))
        phonebook_command(message)
    else:
        lg.write_data(f'Зафиксирован не корректный ввод: {message.text}')
        bot.send_message(chat_id, 'Ты что-то не то ввел')
        phonebook_command(message)


def start_bot():
    print('Server start!')
    bot.polling(none_stop=True)
