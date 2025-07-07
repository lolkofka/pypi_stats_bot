import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import Config


config = Config.load()


def is_admin(user_id: int) -> bool:
    return user_id in config.admins

async def fetch_downloads(package_name: str) -> str:
    url = f"https://pepy.tech/api/v2/projects/{package_name}"
    headers = {
        "X-API-Key": config.pepy_api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                total = data.get("total_downloads", "нет данных")
                return f"📦 {package_name}: {total:,} загрузок"
            else:
                return f"❌ {package_name}: ошибка ({response.status})"


async def cmd_start(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return
    await message.answer("👋 Привет! Напиши /stats чтобы получить статистику загрузок библиотек.")

async def cmd_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён.")
        return
    await message.answer("🔄 Получаю данные...")
    tasks = [fetch_downloads(pkg) for pkg in config.packages]
    results = await asyncio.gather(*tasks)
    await message.answer("📊 Статистика загрузок:\n\n" + "\n".join(results))


async def main():
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_stats, Command("stats"))

    print("✅ Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
