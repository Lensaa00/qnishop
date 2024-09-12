from aiogram import Bot, Router, F

import config
from handlers.main_handlers import database
from keyboards import payment_keyboard as pay_kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.enums import ParseMode

router = Router()
bot = Bot(token=config.TOKEN)


class Payment(StatesGroup):
    amount = State()


def check_payment_amount(amount):
    try:
        amount = float(amount)

        if 100 <= amount <= 10000:
            return True
        else:
            return False
    except ValueError:
        return False


@router.callback_query(F.data == "deposit_balance")
async def deposit_balance_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Payment.amount)
    await callback.message.edit_text(
        text="Введите сумму пополнения:"
    )


@router.message(Payment.amount)
async def deposit_balance_step2(message: Message, state: FSMContext):
    amount = message.text
    if check_payment_amount(amount):
        await state.update_data(amount=amount)
        data = await state.get_data()
        await state.clear()
        await message.answer(
            text=f"<b>Оплата создана</b>\nК оплате: {data['amount']}",
            reply_markup=pay_kb.payment_keyboard(data["amount"]),
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(
            text="Сумма должна быть числом от 100 до 10,000. Попробуйте снова.",
            parse_mode=ParseMode.HTML
        )


@router.callback_query(F.data.contains("payment_agree_"))
async def payment_agree_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    query_string = callback.data.split("_")
    amount = int(query_string[2])
    price = LabeledPrice(label=f"Пополнение баланса на {amount}", amount=amount * 100)

    await bot.send_invoice(
        title="Пополнение баланса",
        chat_id=callback.message.chat.id,
        description="Пополнение баланса QniShop",
        provider_token=config.PAYMASTER,
        currency="RUB",
        prices=[price],
        payload="test-invoice-payload"
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    user_balance = int(database.get_user_balance(str(message.from_user.id)))
    user_balance += round(message.successful_payment.total_amount / 100)
    database.update_user_balance(message.chat.id, str(user_balance))
    await bot.delete_message(message.from_user.id, message.message_id - 1)
    await message.answer(
        text=f"<b>Успешная оплата!</b>\nВаш баланс пополнен на <b>{round(message.successful_payment.total_amount / 100)} Руб.</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=pay_kb.successful_payment_keyboard()
    )
