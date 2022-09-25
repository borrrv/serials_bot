from aiogram.types import (InlineKeyboardButton, 
                            InlineKeyboardMarkup, 
                            KeyboardButton, 
                            ReplyKeyboardMarkup)

"""Главное меню"""
evan = InlineKeyboardButton(text='Еван', callback_data='evan')
roma = InlineKeyboardButton(text='Рома', callback_data='roma')
vlad = InlineKeyboardButton(text='Влад', callback_data='vlad')
mainMenu = InlineKeyboardMarkup(row_width=3).add(evan, roma, vlad)

"""Меню Еван"""
evan_serials = InlineKeyboardButton(text='Мои сериалы', callback_data='evan_serials')
evan_recall = InlineKeyboardButton(text='Вспомнить серию', callback_data='evan_recall')
#evan_new_view = InlineKeyboardButton(text='Добавить просмотр', callback_data='evan_new_view')
evan_new_serial = InlineKeyboardButton(text='Добавить новый сериал', callback_data='evan_new_serial')
evanMenu = InlineKeyboardMarkup(row_width=1).add(evan_serials, evan_recall, evan_new_serial)


"""Меню Рома"""
roma_serials = InlineKeyboardButton(text='Мои сериалы', callback_data='roma_serials')
roma_recall = InlineKeyboardButton(text='Вспомнить серию', callback_data='roma_recall')
#roma_new_view = InlineKeyboardButton(text='Добавить просмотр', callback_data='roma_new_view')
roma_new_serial = InlineKeyboardButton(text='Добавить новый сериал', callback_data='roma_new_serial')
romaMenu = InlineKeyboardMarkup(row_width=1).add(roma_serials, roma_recall, roma_new_serial)

"""Меню Влад"""
vlad_serials = InlineKeyboardButton(text='Мои сериалы', callback_data='vlad_serials')
vlad_recall = InlineKeyboardButton(text='Вспомнить серию', callback_data='vlad_recall')
#vlad_new_view = InlineKeyboardButton(text='Добавить просмотр', callback_data='vlad_new_view')
vlad_new_serial = InlineKeyboardButton(text='Добавить новый сериал', callback_data='vlad_new_serial')
vladMenu = InlineKeyboardMarkup(row_width=1).add(vlad_serials, vlad_recall, vlad_new_serial)

"""Выбор сериала Еван"""
evan_choice = InlineKeyboardButton(text='Выбери сериал', callback_data='evan_choice')
evanChoice = InlineKeyboardMarkup(row_width=1).add(evan_choice)

"""Выбор сериала Влад"""
vlad_choice = InlineKeyboardButton(text='Просмотренные серии', callback_data='vlad_choice')
vladChoice = InlineKeyboardMarkup(row_width=1).add(vlad_choice)

"""Выбор сериала Рома"""
roma_choice = InlineKeyboardButton(text='Выбери сериал', callback_data='roma_choice')
romaChoice = InlineKeyboardMarkup(row_width=1).add(roma_choice)

