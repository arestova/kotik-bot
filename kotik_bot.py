import random
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "data.json"

# Добавь сюда file_id стикеров
STICKERS = [
    "CAACAgIAAxkBAAFHGUFp3J1Rmovvz9UNAo0XiGUi9gm7MAACtzQAAuYZwUjk-aNmkK1pyjsE",
    "CAACAgIAAxkBAAFHGRdp3JvXFrMAAY-_aQS-4uJ85HpLSAsAAjo5AALrIKhJPGMCiIgKPL07BA", "CAACAgIAAxkBAAFHGS1p3JykafREn7YnD68mCnv53ww2fAACwYoAAmxsMUkqrVvLnHBMZTsE", "CAACAgIAAxkBAAFHGS9p3JzEWFDrzoC_-HN_0CStiwbF4gACAZUAAh2qSEvl6SoyOB9NhDsE", "CAACAgIAAxkBAAFHGTFp3Jza0AgdNmi6C4xHyMzRk5qUkgACdIcAAripKUustXlqV2VPwzsE", "CAACAgIAAxkBAAFHGTVp3Jzt59_rquzyWV4LdMbwlWEpvgACSkQAAmH-8UjqblwQzSB_TTsE", "CAACAgIAAxkBAAFHGTdp3J0EisZb3OVDgEOyj85VRoVF2QACAYUAAovlOUkzDjp1Ua9XuzsE", "CAACAgIAAxkBAAFHGTpp3J0XXBl5cjNk8c4UXAiroFI8-QAC84UAAoH2OUkEVmMY_5u8KDsE", "CAACAgIAAxkBAAFHGTxp3J0qLQnuGJjv8D6R8wIQeOcPPgACL44AArkbOElaWjcgDlJaDDsE", "CAACAgIAAxkBAAFHGT9p3J06aJpBx4EK7gwYt28Bo2flyAAC00YAAh9LWUjYT8on3EHEZzsE"
]



# ---------- Работа с данными ----------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"participants": [], "history": {}, "stats": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ---------- Вспомогательные функции ----------
def format_mention(user):
    if user.get("username"):
        return f"@{user['username']}"
    return user["name"]


# ---------- Команды ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()

    participant = {
        "id": user.id,
        "name": user.first_name,
        "username": user.username,
    }

    if not any(p["id"] == user.id for p in data["participants"]):
        data["participants"].append(participant)
        save_data(data)
        text = (
            "Привет! 🐱\n\n"
            "Я выбираю котика дня.\n"
            "Ты зарегистрирован для участия!\n\n"
            "Доступные команды:\n"
            "/kotik_of_the_day — выбрать котика дня\n"
            "/kotik_stats — посмотреть статистику"
        )
    else:
        text = "Ты уже участвуешь! 😺"

    await update.message.reply_text(text)


async def kotik_of_the_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    participants = data["participants"]

    if not participants:
        await update.message.reply_text(
            "Нет участников. Попросите пользователей отправить /start."
        )
        return

    today = datetime.now().strftime("%Y-%m-%d")

    # Проверяем, выбран ли котик сегодня
    if today in data["history"]:
        record = data["history"][today]
        winner = record["winner"]
        sticker = record.get("sticker")

        mention = format_mention(winner)

        # Отправляем тот же стикер
        if sticker:
            await update.message.reply_sticker(sticker)

        await update.message.reply_text(
            f"🐱 Сегодняшний котик дня уже выбран — {mention}!"
        )
        return

    # Выбираем победителя и стикер
    winner = random.choice(participants)
    sticker = random.choice(STICKERS) if STICKERS else None

    # Сохраняем результат дня
    data["history"][today] = {
        "winner": winner,
        "sticker": sticker
    }

    # Обновляем статистику
    user_id = str(winner["id"])
    data["stats"][user_id] = data["stats"].get(user_id, 0) + 1
    save_data(data)

    mention = format_mention(winner)

    # Отправляем стикер
    if sticker:
        await update.message.reply_sticker(sticker)

    # Отправляем сообщение
    await update.message.reply_text(
        f"🐱 Сегодня котик дня — {mention}!"
    )


async def kotik_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    participants = data.get("participants", [])
    stats = data.get("stats", {})

    if not participants:
        await update.message.reply_text(
            "Пока нет зарегистрированных участников."
        )
        return

    # Формируем полный список участников со значением 0 по умолчанию
    full_stats = []
    for participant in participants:
        user_id = str(participant["id"])
        wins = stats.get(user_id, 0)

        # Отображаем username без тега или имя
        display_name = (
    participant.get("username")
    if participant.get("username")
    else participant.get("name", "Unknown")
)

        full_stats.append((display_name, wins))

    # Сортируем по количеству побед (по убыванию)
    full_stats.sort(key=lambda x: x[1], reverse=True)

    # Формируем текст ответа
    text = "📊 Статистика котиков дня:\n\n"
    for name, wins in full_stats:
        text += f"{name} — {wins} 🐱\n"

    await update.message.reply_text(text)


# ---------- Запуск бота ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kotik_of_the_day", kotik_of_the_day))
    app.add_handler(CommandHandler("kotik_stats", kotik_stats))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
