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
        text='Приветствие, описание бота", как вас зовут?')

    await state.set_state(StatesContext.enter_name_data)


@router.message(StatesContext.enter_name_data)
async def handle_enter_name_data(message: Message, state: FSMContext):
    await message.answer(text='Выберите необходимую услугу',
                         reply_markup=choose_service_markup)
    await state.update_data(name_data=message.text)
    await state.set_state(StatesContext.choose_service)


@router.callback_query(F.data == 'fulfillment_start')
async def callback_fulfillment_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Оставьте свой рабочий телефон, для того, чтобы наш менеджер уточнил все детали")
    await state.update_data(service='fulfillment')
    await state.set_state(StatesContext.enter_contact_data_bitrix)


@router.message(StatesContext.enter_contact_data_bitrix)
async def callback_enter_name_data(message: Message, state: FSMContext):
    await message.answer(text='Если вы хотите сразу что-то уточнить, оставьте примечание',
                         reply_markup=finish_markup)
    await state.update_data(contact_data=message.text)
    await state.set_state(StatesContext.final)


@router.callback_query(F.data == 'fulfillment_start')
async def callback_fulfillment_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Оставьте свой рабочий телефон, для того, чтобы наш менеджер уточнил все детали")
    await state.update_data(service='fulfillment')
    await state.set_state(StatesContext.enter_contact_data_bitrix)


@router.message(StatesContext.enter_contact_data_china)
async def callback_enter_name_data(message: Message, state: FSMContext):
    await message.answer(text='Если вы хотите сразу что-то уточнить, оставьте примечание',
                         reply_markup=finish_markup)
    await state.update_data(contact_data=message.text)
    await state.set_state(StatesContext.final)


async def _finish(message: Message, data):
    await message.answer(text='Ваши данные переданы менеджеру')
    await message.answer_document(document=FSInputFile('data/Фулфилмент полного цикла.pdf'))
    if data['service'] == 'fulfillment':
        await message.answer_document(document=FSInputFile('data/Прайс.pdf'))
    print(data)
    await bx.call('tasks.task.add',
        {
            'fields': {
                'TITLE': 'Opachki',
                'DESCRIPTION': 'dannie',
                'CREATED_BY': 1,
                'RESPONSIBLE_ID': 1
            }
        })


@router.callback_query(F.data == 'finish', StatesContext.final)
async def callback_final(callback: CallbackQuery, state: FSMContext):
    await _finish(callback.message, await state.get_data())
    await state.set_state(StatesContext.done)


@router.message(StatesContext.final)
async def callback_finish(message: Message, state: FSMContext):
    await _finish(message, await state.get_data())
    await state.set_state(StatesContext.done)
