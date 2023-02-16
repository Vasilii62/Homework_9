from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)
but_s_1 = KeyboardButton('/tic_tac_toe')
but_s_2 = KeyboardButton('/calc')
but_s_3 = KeyboardButton('/phonebook')
but_s_4 = KeyboardButton('/help')
keyboard_start.add(but_s_1, but_s_2).add(but_s_3, but_s_4)


# keyboard_tic_tac = InlineKeyboardMarkup(row_width=3)
# ib_1 = InlineKeyboardButton(' ', callback_data='1')
# ib_2 = InlineKeyboardButton(' ', callback_data='2')
# ib_3 = InlineKeyboardButton(' ', callback_data='3')
# ib_4 = InlineKeyboardButton(' ', callback_data='4')
# ib_5 = InlineKeyboardButton(' ', callback_data='5')
# ib_6 = InlineKeyboardButton(' ', callback_data='6')
# ib_7 = InlineKeyboardButton(' ', callback_data='7')
# ib_8 = InlineKeyboardButton(' ', callback_data='8')
# ib_9 = InlineKeyboardButton(' ', callback_data='9')
# keyboard_tic_tac.add(ib_1, ib_2, ib_3, ib_4, ib_5, ib_6, ib_7, ib_8, ib_9)


keyboard_phonebook = InlineKeyboardMarkup(row_width=1)
ibp_1 = InlineKeyboardButton('Добавить контакт', callback_data='Добавить контакт')
ibp_2 = InlineKeyboardButton('Найти контакт', callback_data='Найти контакт')
ibp_3 = InlineKeyboardButton('Удалить контакт', callback_data='Удалить контакт')
ibp_4 = InlineKeyboardButton('Показать справочник', callback_data='Показать справочник')
ibp_5 = InlineKeyboardButton('Импортировать справочник', callback_data='Импортировать справочник')
ibp_6 = InlineKeyboardButton('Экспортировать справочник', callback_data='Экспортировать справочник')
ibp_7 = InlineKeyboardButton('Выход', callback_data='Выход')
keyboard_phonebook.add(ibp_1, ibp_2, ibp_3, ibp_4, ibp_5, ibp_6, ibp_7)

def update_keyboard_tic_tac(list_text, list_callback):
    keyboard_tic_tac_up = InlineKeyboardMarkup(row_width=3)
    for i in range(0, 9, 3):
        keyboard_tic_tac_up.row(InlineKeyboardButton(text=list_text[i], callback_data=list_callback[i]),
                                InlineKeyboardButton(text=list_text[i+1], callback_data=list_callback[i+1]),
                                InlineKeyboardButton(text=list_text[i+2], callback_data=list_callback[i+2]))
    return keyboard_tic_tac_up



