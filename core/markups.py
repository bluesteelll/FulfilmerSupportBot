from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

# Keyboards and markups

choose_service_keys = [
    [InlineKeyboardButton(text='Фулфилмент',
                          callback_data='fulfillment_start')],
    [InlineKeyboardButton(text='Доставка из Китая',
                          callback_data='china_start')]]

finish_keys = [
    [InlineKeyboardButton(text='Оставить заявку 🚀',
                          callback_data='finish')]]

choose_service_markup = InlineKeyboardMarkup(inline_keyboard=choose_service_keys)
finish_markup = InlineKeyboardMarkup(inline_keyboard=finish_keys)
