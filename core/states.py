from aiogram.fsm.state import StatesGroup, State


class StatesContext(StatesGroup):
    enter_name_data = State()
    choose_service = State()
    start_china = State()
    start_bitrix = State()
    enter_contact_data_china = State()
    enter_contact_data_bitrix = State()
    final_china = State()
    final_bitrix = State()
    finish = State()
    done = State()
    final = State()
    item_count = State()

