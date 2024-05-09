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
        text='Команда FulFilmer приветствует Вас!\nВы находитесь в боте оформления запроса на сотрудничество с нашей '
             'компанией.\nВ начале напишите пожалуйста Ваше полное имя')

    await state.set_state(StatesContext.enter_name_data)


@router.message(StatesContext.enter_name_data)
async def handle_enter_name_data(message: Message, state: FSMContext):
    await message.answer(text='Отлично!\nТеперь Вам необходимо выбрать интересующую услугу',
                         reply_markup=choose_service_markup)
    await state.update_data(name=message.text)
    await state.set_state(StatesContext.choose_service)


@router.callback_query(F.data == 'fulfillment_start')
async def callback_fulfillment_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Вас интересует фулфилмент\bОставьте пожалуйста одним сообщением ваши рабочие контакты, чтобы наш "
             "менеджер уточнил все детали")
    await state.update_data(service='fulfillment')
    await state.set_state(StatesContext.enter_contact_data_bitrix)


@router.message(StatesContext.enter_contact_data_bitrix)
async def callback_enter_name_data_bitrix(message: Message, state: FSMContext):
    await message.answer(text='Все почти готово\nНажмите на кнопку "Отправить", либо напишите сообщение, если вы '
                              'хотите что-либо уточнить сразу',
                         reply_markup=finish_markup)
    await state.update_data(contact=message.text)
    await state.set_state(StatesContext.final)


@router.callback_query(F.data == 'china_start')
async def callback_china_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Вас интересует доставка из Китая\bОставьте пожалуйста одним сообщением ваши рабочие контакты, чтобы наш "
             "менеджер уточнил все детали")
    await state.update_data(service='china')
    await state.set_state(StatesContext.enter_contact_data_china)


@router.message(StatesContext.enter_contact_data_china)
async def callback_enter_name_data_china(message: Message, state: FSMContext):
    await message.answer(text='Все почти готово\nНажмите на кнопку "Отправить", либо напишите сообщение, если вы '
                              'хотите что-либо уточнить сразу',
                         reply_markup=finish_markup)
    await state.update_data(contact=message.text)
    await state.set_state(StatesContext.final)


@router.callback_query(F.data == 'finish', StatesContext.final)
async def callback_final(callback: CallbackQuery, state: FSMContext):
    await state.update_data(comment='No comment')
    await _finish(callback.message, await state.get_data())
    await state.set_state(StatesContext.done)


@router.message(StatesContext.final)
async def callback_finish(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await _finish(message, await state.get_data())
    await state.set_state(StatesContext.done)


async def _finish(message: Message, data):
    await message.answer(text='Все готово\nВаш запрос сформирован и отправлен\nСейчас вам будут отправлены PDF файлы '
                              'для преварительного ознакомления\nНадеемся на благотворное сотрудничество!')
    await message.answer_document(document=FSInputFile('data/Фулфилмент полного цикла.pdf'))
    if data['service'] == 'fulfillment':
        await message.answer_document(document=FSInputFile('data/Прайс.pdf'))
    print(data)
    await bx.call('tasks.task.add',
                  {
                      'fields': {
                          'TITLE': f'Запрос клиента {data['name']}',
                          'DESCRIPTION': f'Имя:\t{data['name']}\nУслуга:\t{data['service']}\nКонтакты:\t{data['contact']}\n'
                                         f'Комментарий:\t{data['comment']}',
                          'CREATED_BY': 1,
                          'RESPONSIBLE_ID': 1
                      }
                  })


@router.message(F.text.lower().regexp(r'(.*прайс*.)|(.*цена*.)|(.*сколько*.)|(.*доставка*.)|(.*кита*.)|(.*фулфилмент*.)|(.*отгрузка*.)|(.*поставка*.)|(.*условия*.)|(.*услуги*.)|(.*узнать*.)|(.*можно*.)|(.*заказать*.)|(.*юан*.)|(.*поиск*.)|(.*Добрый*.)|(.*товар*.)|(.*сотрудничеств*.)'))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply(
        text='Здравствуйте 👋\nНапишите мне, чтобы узнать условия и получить прайс:\n@fulfilmer_support_bot')
