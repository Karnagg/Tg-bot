#API_TOKEN = "8471456341:AAEWzxu3UH1R9EmSNGDa4mEj_dRKHPyTbzY"
#OWNER_ID = 2039219427  #6187029881 ← твой Telegram ID
import asyncio
import json
import os
import random
import string
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.client.default import DefaultBotProperties

API_TOKEN = "8471456341:AAEWzxu3UH1R9EmSNGDa4mEj_dRKHPyTbzY"
ADMIN_IDS = [2039219427, 6187029881]

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ========== СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЯ ==========
user_states = {}

# ========== ГЛАВНОЕ МЕНЮ ==========
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Обучение"), KeyboardButton(text="💰 Способы заработка")],
        [KeyboardButton(text="⚠️ Виды скама"), KeyboardButton(text="📊 Актуальные проекты")],
        [KeyboardButton(text="🧾 Глоссарий"), KeyboardButton(text="🛠 Инструменты")],
        [KeyboardButton(text="📩 Оставить отзыв"), KeyboardButton(text="🥼 Политика конфиденциальности")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите раздел"
)
#Политика конфиденциальности
# ========== ПОДМЕНЮ ОБУЧЕНИЯ ==========
education_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Что такое Криптовалюта?")],
        [KeyboardButton(text="Как купить криптовалюту")],
        [KeyboardButton(text="Основы безопасности")],
        [KeyboardButton(text="Кошелёк")],
        [KeyboardButton(text="◀️ Назад")]
    ],
    resize_keyboard=True
)

# ========== БАЗОВЫЕ ФУНКЦИИ ==========
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

users_db = load_users()

def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

# ========== ОБРАБОТЧИКИ КОМАНД ==========
@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = str(message.from_user.id)

    if user_id in users_db and users_db[user_id]["verified"]:
        await message.answer(
            "✅ Вы уже авторизованы.",
            reply_markup=main_menu_kb
        )
        return

    if user_id not in users_db:
        password = generate_password()
        users_db[user_id] = {
            "password": password,
            "verified": False
        }
        save_users(users_db)

        text = (
            f"🆕 Новый пользователь!\n"
            f"👤 ID: <code>{user_id}</code>\n"
            f"🔑 Пароль: <code>{password}</code>"
        )
        for admin_id in ADMIN_IDS:
            await bot.send_message(admin_id, text)

        await message.answer(
            "⛔ Нет доступа. Введите выданный вам пароль.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "⛔ Введите свой пароль для доступа.",
            reply_markup=ReplyKeyboardRemove()
        )

@dp.message(Command("menu"))
async def menu_handler(message: Message):
    user_id = str(message.from_user.id)
    
    if user_id not in users_db or not users_db[user_id]["verified"]:
        return await message.answer("⛔ Сначала авторизуйтесь через /start")
    
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb
    )

# ========== ОБРАБОТКА МЕНЮ ==========
@dp.message()
async def message_handler(message: Message):
    user_id = str(message.from_user.id)
    text = message.text

    # Если пользователь не авторизован
    if user_id not in users_db or not users_db[user_id]["verified"]:
        return await password_handler(message)
    
    # Обработка главного меню
    if text == "📚 Обучение":
        user_states[user_id] = "in_education_menu"
        await message.answer("Выберите тему обучения:", reply_markup=education_menu_kb)
    
    # Обработка подменю обучения
    elif user_states.get(user_id) == "in_education_menu":
        if text == "◀️ Назад":
            user_states[user_id] = None
            await message.answer("Главное меню:", reply_markup=main_menu_kb)
        elif text == "Что такое Криптовалюта?":
            response = (
                "💰 <b>Криптовалюта</b> — это цифровая форма денег, созданная на базе блокчейн-технологии. "
                "Она не контролируется банками или государствами.\n\n"
                "🔹 <b>Примеры:</b>\n"
                "- Bitcoin (BTC) — первая и самая популярная\n"
                "- Ethereum (ETH) — с умными контрактами\n"
                "- USDT, USDC — «стейблкоины», привязаны к доллару\n\n"
                "📌 <i>Используется для:</i>\n"
                "- Переводов\n"
                "- Инвестиций\n"
                "- Торговли\n"
                "- Участия в Web3\n\n"
                "🔹 <b>Что такое блокчейн?</b>\n"
                "Это база данных, которая работает как «цепочка блоков». Каждый блок содержит информацию "
                "о транзакциях и связан с предыдущим.\n\n"
                "🔹 <b>Особенности:</b>\n"
                "- Прозрачен для всех\n"
                "- Нельзя удалить или изменить прошлые данные\n"
                "- Надёжность за счёт распределённости (тысячи узлов подтверждают данные)\n\n"
                "🔹 <b>В чём смысл криптовалют?</b>\n"
                "🔒 Свобода от банков и централизации\n"
                "🌐 Глобальные переводы без посредников\n"
                "🛠 Доступ к новым Web3-приложениям\n"
                "💰 Инвестирование и спекуляции\n"
                "💡 Участие в децентрализованных системах (DeFi, DAO)\n\n"
                "🔹 <b>Чем коин отличается от токена?</b>\n"
                "<b>Коин (coin)</b> — работает на собственном блокчейне (BTC, ETH, TON)\n"
                "<b>Токен (token)</b> — выпускается на чужом блокчейне (чаще Ethereum, Arbitrum)\n\n"
                "📌 <b>Типы токенов:</b>\n"
                "- Utility (полезность)\n"
                "- Governance (голосование)\n"
                "- Security (как акции)"
            )
            await message.answer(response, reply_markup=education_menu_kb)
        elif text == "Как купить криптовалюту":
            await message.answer("Информация о покупке криптовалюты...", reply_markup=education_menu_kb)
        elif text == "Основы безопасности":
            await message.answer("Информация о безопасности...", reply_markup=education_menu_kb)
        elif text == "Кошелёк":
            response = (
                "💼 <b>Что такое криптокошелёк?</b>\n\n"
                "Это инструмент для хранения и управления криптовалютами. По сути - ваш личный банк в мире крипты.\n\n"
                "🔹 <b>Основные типы кошельков:</b>\n\n"
                "🔥 <b>Горячие кошельки</b> (онлайн, удобные для частых операций):\n"
                "- MetaMask — браузерный (поддерживает ETH и токены ERC-20)\n"
                "- Trust Wallet — мобильный, поддерживает множество сетей\n"
                "- Phantom — для Solana и SPL-токенов\n"
                "- WalletConnect — универсальный кошелёк для DeFi\n\n"
                "❄️ <b>Холодные кошельки</b> (оффлайн, максимальная безопасность):\n"
                "- Ledger Nano S/X — аппаратные кошельки\n"
                "- Trezor — ещё один популярный аппаратный вариант\n"
                "- Paper Wallet — распечатанные приватные ключи\n\n"
                "🔐 <b>Как выбрать кошелёк?</b>\n"
                "1. Определите нужные вам блокчейны\n"
                "2. Решите, как часто будете совершать операции\n"
                "3. Оцените сумму хранения (большие суммы — только холодные кошельки!)\n\n"
                "⚠️ <b>Важно!</b> Никогда не храните приватные ключи в интернете и не делитесь seed-фразой!"
            )
            await message.answer(response, reply_markup=education_menu_kb)


    # Обработка других пунктов главного меню
    elif text == "💰 Способы заработка":
        await message.answer("Раздел в разработке", reply_markup=main_menu_kb)
    elif text == "⚠️ Виды скама":
        await message.answer("Раздел в разработке", reply_markup=main_menu_kb)
    elif text == "📊 Актуальные проекты":
        await message.answer("Раздел в разработке", reply_markup=main_menu_kb)
    elif text == "🧾 Глоссарий":
        await message.answer("Раздел в разработке", reply_markup=main_menu_kb)
    elif text == "🛠 Инструменты":
        await message.answer(
        "1. CoinMarketCap\n"
        "coinmarketcap.com\n"
        "Главный сайт для отслеживания цен, рейтингов и рыночной капитализации криптовалют.\n\n"
        
        "2. CoinGecko\n"
        "coingecko.com\n"
        "Аналог CoinMarketCap с дополнительными метриками, графиками и статистикой.\n\n"
        
        "3. Etherscan\n"
        "etherscan.io\n"
        "Блокчейн-эксплорер для Ethereum — проверяй транзакции, контракты, адреса.\n\n"

        "4. DeBank\n"
        "debank.com\n"
        "Твой крипто-портфель и аналитика DeFi-проектов, займы, стейкинг.\n\n"
        
        "5. Uniswap\n"
        "uniswap.org\n"
        "Популярная децентрализованная биржа (DEX) для обмена токенов на Ethereum.\n\n"
        
        "6. MetaMask\n"
        "metamask.io\n"
        "Браузерный кошелек для Ethereum и совместимых блокчейнов.\n\n"

        "7. Zealy\n"
        "zealy.io)\n"
        "Платформа для выполнения крипто-заданий, участия в airdrop и проектах.\n\n"

        "8. Dextools\n"
        "dextools.io\n"
        "Анализ и мониторинг новых токенов на децентрализованных биржах.\n\n"

        "9. Galxe\n"
        "galxe.com\n"
        "Платформа для выполнения заданий и получения наград (airdrop, NFT).\n\n"

        "10. Ledger Live\n"
        "ledger.com/live\n"
        "Официальное приложение для управления криптовалютами на аппаратных кошельках Ledger.\n\n"

        "11. Trust Wallet\n"
        "trustwallet.com\n"
        "Мобильный кошелёк с поддержкой множества блокчейнов и токенов.\n\n"
        
        "12. 1inch\n"
        "1inch.io\n"
        "Агрегатор DEX — ищет лучшие курсы обмена на разных децентрализованных биржах.\n\n"
        
        "13. Zapper\n"
        "zapper.fi\n"
        "Удобный интерфейс для управления DeFi-портфелем и инвестициями.\n\n"
        
        "14. Cryptopanic\n"
        "cryptopanic.com\n"
        "Агрегатор новостей криптомира — чтобы быть в курсе событий.\n\n"
        
        "15. CoinPaprika\n"
        "coinpaprika.com \n"
        "Альтернатива CoinMarketCap с дополнительной аналитикой и ICO календарём.\n\n"
    )
    elif text == "🥼 Политика конфиденциальности":
        await message.answer("" \
        "🚫 Запрещено:" \
        "1. Распространять любую информацию из этого бота(скрины, файлы). "
        "2. Любое нарушение конфиденциальности = мгновенный бан без предупреждений." \
        "3. Обжаловать бан можно здесь -- @zxc_admin993 ")
    elif text == "📩 Оставить отзыв":
        await message.answer("Отзыв можно оставить здесь --- https://t.me/+iFEDdF8sJt03NjUy", reply_markup=main_menu_kb)
    else:
        await message.answer("❌ Неизвестная команда", reply_markup=main_menu_kb)

async def password_handler(message: Message):
    user_id = str(message.from_user.id)
    

    if user_id not in users_db:
        await message.answer("⚠️ Пожалуйста, напишите /start сначала.")
        return

    if users_db[user_id]["verified"]:
        await message.answer("✅ Вы уже авторизованы.", reply_markup=main_menu_kb)
        return

    entered_password = message.text.strip()
    correct_password = users_db[user_id]["password"]

    if entered_password == correct_password:
        users_db[user_id]["verified"] = True
        save_users(users_db)
        await message.answer(
            "✅ Пароль принят! Добро пожаловать.",
            reply_markup=main_menu_kb
        )
    else:
        await message.answer("❌ Неверный пароль, попробуйте снова.")

async def main():
    print("🤖 Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())