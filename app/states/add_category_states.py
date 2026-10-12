from aiogram.fsm.state import StatesGroup,State
class AddCategoryStates(StatesGroup):
    name=State()
    type=State()