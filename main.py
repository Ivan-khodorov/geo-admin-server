import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.Config import Config
from bot.set_bot_commands import set_default_commands
from bot.handlers import object_search  # добавлен новый router
from bot.handlers import done, route_report, register_admin, city_picker, next_point
from bot.handlers import start, search, scheduler
from bot.handlers import admin_zone
from bot.handlers import admin_zone_extension
from save_zone import app

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(admin_zone_extension.router)
dp.include_router(start.router)
dp.include_router(done.router)
dp.include_router(route_report.router)
dp.include_router(register_admin.router)
dp.include_router(city_picker.router)
dp.include_router(next_point.router)
dp.include_router(search.router)
dp.include_router(object_search.router)  # регистрация
dp.include_router(admin_zone.router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await scheduler.setup_scheduler(bot)
    await set_default_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
