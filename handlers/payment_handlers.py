from aiogram import Bot, Router, F

import config
from keyboards import payment_keyboard as pay_kb
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment
from aiogram.enums import ParseMode, ContentType

router = Router()
bot = Bot(token=config.TOKEN)


class Payment(StatesGroup):
    amount = State()


@router.callback_query(F.data == "deposit_balance")
async def deposit_balance_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Payment.amount)
    await callback.message.edit_text(
        text="Введите сумму пополнения:"
    )


@router.message(Payment.amount)
async def deposit_balance_step2(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    data = await state.get_data()
    await message.answer(
        text=f"<b>Чек создан</b>\nК оплате: {data["amount"]}",
        reply_markup=pay_kb.payment_keyboard(data["amount"]),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.contains("payment_agree_"))
async def payment_agree_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
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


@router.message(F.contains(SuccessfulPayment))
async def successful_payment(message: Message, state: FSMContext):
    await message.answer(
        text=f"<b>Успешная оплата!</b>\nВы получили {message.successful_payment.total_amount} Руб."
    )
