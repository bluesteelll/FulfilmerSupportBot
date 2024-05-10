from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from core.states import StatesContext
from core.markups import choose_service_markup, finish_markup
from fast_bitrix24 import Bitrix
from data.config import BITRIX_WEBHOOK

router = Router()
bx = Bitrix(webhook=BITRIX_WEBHOOK)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        text='🤝Давайте познакомимся, как я могу к вам обращаться ?')

    await state.set_state(StatesContext.enter_name_data)


@router.message(StatesContext.enter_name_data)
async def handle_enter_name_data(message: Message, state: FSMContext):
    await message.answer(text=f'✅Отлично, {message.text}.\nВыберите направление которое вас интересует',
                         reply_markup=choose_service_markup)
    await state.update_data(name=message.text)
    await state.set_state(StatesContext.choose_service)


@router.callback_query(F.data == 'fulfillment_start')
async def callback_fulfillment_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="✍️Укажите категорию и кол-во товара одним сообщением.")
    await state.update_data(service='ФФ')
    await state.set_state(StatesContext.item_count)


@router.message(StatesContext.item_count)
async def callback_fulfillment_start(message: Message, state: FSMContext):
    await message.answer(
        text="☎️ Оставьте свои контактные данные, чтобы рассчитать индивидуальное предложение.\nНаш специалист свяжется с вами в ближайшее время")
    await state.update_data(item_count=message.text)
    await state.set_state(StatesContext.enter_contact_data_bitrix)


@router.message(StatesContext.enter_contact_data_bitrix)
async def callback_enter_name_data_bitrix(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(StatesContext.final)
    await _finish(message, await state.get_data())


@router.callback_query(F.data == 'china_start')
async def callback_fulfillment_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="✍️Укажите категорию и кол-во товара одним сообщением.")
    await state.update_data(service='китай')
    await state.set_state(StatesContext.item_count)


@router.message(StatesContext.item_count)
async def callback_fulfillment_start(message: Message, state: FSMContext):
    await message.answer(
        text="☎️ Оставьте свои контактные данные, чтобы рассчитать индивидуальное предложение.\nНаш специалист свяжется с вами в ближайшее время")
    await state.update_data(item_count=message.text)
    await state.set_state(StatesContext.enter_contact_data_bitrix)


@router.message(StatesContext.enter_contact_data_china)
async def callback_enter_name_data_china(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(StatesContext.final)
    await _finish(message, await state.get_data())


async def _finish(message: Message, data):
    await message.answer(
        text='✈️Заявка на расчет уже у менеджера!\nА пока вы ожидаете звонок, можете ознакомится с информацией о нашей компании')
    await message.answer_document(document=FSInputFile(r'data/Fulfilmer – О нас.pdf'))
    if data['service'] == 'ФФ':
        await message.answer_document(document=FSInputFile(r'data/Fulfilmer – Прайс.pdf'))
    await bx.call('crm.lead.add',
                  {
                      'fields': {
                          'TITLE': f'{data['name']} — тг-бот ({data['service']})',
                          'NAME': data['name'],
                          "PHONE": [{"VALUE": data['contact']}],
                          'COMMENTS': data['item_count']}
                  })


@router.message(F.text.lower().regexp(
    r'(.*прайс*.)|(.*цена*.)|(.*сколько*.)|(.*доставка*.)|(.*кита*.)|(.*фулфилмент*.)|(.*отгрузка*.)|(.*поставка*.)|(.*условия*.)|(.*услуги*.)|(.*узнать*.)|(.*можно*.)|(.*заказать*.)|(.*юан*.)|(.*поиск*.)|(.*Добрый*.)|(.*товар*.)|(.*сотрудничеств*.)'))
async def chat_reply(message: Message, state: FSMContext):
    await message.reply(
        text='Здравствуйте 👋\nНапишите мне, чтобы узнать условия и получить прайс:\n@fulfilmer_support_bot')
