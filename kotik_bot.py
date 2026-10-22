import random
import json
import os
import subprocess
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "data.json"

STICKERS = [
    "CAACAgIAAxkBAAFHGUFp3J1Rmovvz9UNAo0XiGUi9gm7MAACtzQAAuYZwUjk-aNmkK1pyjsE",
    "CAACAgIAAxkBAAFHGRdp3JvXFrMAAY-_aQS-4uJ85HpLSAsAAjo5AALrIKhJPGMCiIgKPL07BA",
    "CAACAgIAAxkBAAFHGS1p3JykafREn7YnD68mCnv53ww2fAACwYoAAmxsMUkqrVvLnHBMZTsE",
    "CAACAgIAAxkBAAFHGS9p3JzEWFDrzoC_-HN_0CStiwbF4gACAZUAAh2qSEvl6SoyOB9NhDsE",
    "CAACAgIAAxkBAAFHGTFp3Jza0AgdNmi6C4xHyMzRk5qUkgACdIcAAripKUustXlqV2VPwzsE",
    "CAACAgIAAxkBAAFHGTVp3Jzt59_rquzyWV4LdMbwlWEpvgACSkQAAmH-8UjqblwQzSB_TTsE",
    "CAACAgIAAxkBAAFHGTdp3J0EisZb3OVDgEOyj85VRoVF2QACAYUAAovlOUkzDjp1Ua9XuzsE",
    "CAACAgIAAxkBAAFHGTpp3J0XXBl5cjNk8c4UXAiroFI8-QAC84UAAoH2OUkEVmMY_5u8KDsE",
    "CAACAgIAAxkBAAFHGTxp3J0qLQnuGJjv8D6R8wIQeOcPPgACL44AArkbOElaWjcgDlJaDDsE",
    "CAACAgIAAxkBAAFHGT9p3J06aJpBx4EK7gwYt28Bo2flyAAC00YAAh9LWUjYT8on3EHEZzsE",
    "CAACAgIAAxkBAAEv9Pxq2ls5h49QzBNiB10GxWW5OQXHngAC5G8AAnnlKEoIZfLtKNtLfD0E",
    "CAACAgIAAxkBAAEv9P5q2ltjD-pmbebUrWXicxrWv-aRbAACG5AAAqyTsEg9RU2HEtJSsz0E",
    "CAACAgIAAxkBAAEv9QABatpbuXzzDT45BGWeWtChphaDnVcAAnaOAAKLQ2BKjpGiMewo8Q89BA",
    "CAACAgIAAxkBAAEv9QRq2lvSqeclAAHbNnuquF01xeQD658AAgGCAAJX9LhI29eCwWAXSPI9BA",
    "CAACAgIAAxkBAAEv9QZq2lvnOdcX8tHnrtX2AAGRA_CnVCUAArSOAALbFLlIDisEDYE251g9BA",
    "CAACAgIAAxkBAAEv9Qhq2lvyBqYEKmNN3hiVjBepasJ3vgACbYwAAqdquEhQOfxz3_dzlz0E",
    "CAACAgIAAxkBAAEv9Qpq2lwSLFn1Qu8zYp_0LMN9xtKB2gACooIAAuQd2Ugn9UJGjMIOgT0E",
    "CAACAgIAAxkBAAEv9Q5q2lwkT_kLYGdKkKBvfoOBnr0eLAAC4JMAAgtiuUir8wGsXeW6dj0E",
    "CAACAgIAAxkBAAEv9RBq2lw9Ir2K1wE3I93bvodAGUO8QgAC548AAqv4WUpP7URY-XTSQD0E",
    "CAACAgIAAxkBAAEv9RJq2lx3QFBJLEpg4jIKlbVpKGIcEAAC_psAAnQ8WUvWWQpP7l0sTD0E",
    "CAACAgIAAxkBAAEv9RRq2lyQDMottlxWV_IXcA50TBYCvgAC2YUAAmhWOEqMrjADgrgXUT0E",
    "CAACAgIAAxkBAAEv9RZq2lycqDW_89QiLE4Sl_DOcZwFSAACFEEAAiUv0EtQklt6hfYNPT0E",
    "CAACAgIAAxkBAAEv9Rpq2lzCqPVXLC7sFicxCFp2t5aOPQACIwMAAhM5jxGGj5HtRkkgzD0E",
    "CAACAgIAAxkBAAEv9Rxq2lzfgFZ8xWclgCBz8LNku2LQjgACRBQAAjOHQEvwpfRdkvwMKT0E",
    "CAACAgIAAxkBAAEv9SBq2l1EHJyGMPTQRZzBx9Z-yBEQ2QACeQcAAkVRkw6YdmPl068Ilj0E",
    "CAACAgIAAxkBAAEv9SJq2l1c52l0dkc4cq--5P-oXVMBmwACqwcAAkVRkw7ZYYCtA3gsgj0E",
    "CAACAgIAAxkBAAEv9SRq2l1zb_wgQn21eK1Nv4NoJb1TggAC9AcAAkVRkw5yesWcsVEsBz0E",
    "CAACAgIAAxkBAAEv9SZq2l2Hlt1QjhM3NvbOgxIO9DfL5QAC-QcAAkVRkw5hy_55YtUgRj0E",
    "CAACAgIAAxkBAAEv9Shq2l2XvlyHuCrEB-rcvFfQdjYrbgACGQgAAkVRkw4YtnSJxzLcFz0E",
    "CAACAgIAAxkBAAEv9Spq2l3bwTX4iLKbJ5896BNw9HsigQACnQgAAkVRkw49IUUnjZX3sT0E",
    "CAACAgIAAxkBAAEv9Sxq2l3rDBbGfzB-MkaZBaCN_xU14wACowgAAkVRkw6APyHQN27GOj0E",
    "CAACAgIAAxkBAAEv9S5q2l37Y96jiq1ZAVLCgqrQ8RVYnQACpAgAAkVRkw4VweUPYtLZQj0E",
    "CAACAgIAAxkBAAEv9TBq2l4vA1KF_3jIdEsov57Rq-MTYgACOhMAAgGPMErlG1EfiD4eDT0E",
    "CAACAgIAAxkBAAEv9TJq2l5BmWVB3TH50zN0EAOFXxtFBgACFqAAApicyUhpX5y-J_PWzj0E",
    "CAACAgIAAxkBAAEv9TRq2l5bYuoKU7XNmrzz1rhqq9N4wAACIgADXQWCFtBPvQdMawHcPQQ",
    "CAACAgIAAxkBAAEv9Thq2l6MoJhynwhCi3dwFcN2jICBvgAC-GcAAtEOKEnvHYJS4zOvLD0E",
    "CAACAgIAAxkBAAEv9Txq2l6uUTAtST8mysIV0xE0Mq1gZQAC9xYAArJByUsY7SYiPNp5hj0E",
    "CAACAgIAAxkBAAEv9UBq2l7oiEwypWw0R4tq-FpiQmfbIwACLwUAAiMFDQABEwABi-vbd5ogPQQ",
    "CAACAgIAAxkBAAEv9UJq2l7_TeHFFhad5gIGl5b0kKl97QAC2gUAAiMFDQABgxgF6ASMVw09BA",
    "CAACAgIAAxkBAAEv9URq2l8OwE79revCI_jYjNGsSzg4awACBAYAAiMFDQABfEW2wKiQPq89BA",
    "CAACAgIAAxkBAAEv9UZq2l8t0wiMaRnubNRjrF6y3yZdjAACpgUAAiMFDQABiPD2mbG1L-E9BA",
    "CAACAgIAAxkBAAEv9Uhq2l9Aov3tQul3wZfa3nm2J5Sv0gACqwUAAiMFDQABBQ5XDl6d4089BA",
    "CAACAgIAAxkBAAEv9Upq2l9Nlp2uQ9TrVUO7q4YQaVuboAACqAUAAiMFDQABZz3Ih7XfFmg9BA",
    "CAACAgIAAxkBAAEv9Uxq2l9ZIy_8T1dnxaUB8m2nvc9_3gACjgUAAiMFDQAB_8ISUCLZ0Q09BA",
    "CAACAgIAAxkBAAEv9VBq2l-CSqKDBIb0-4do1aEIBoV70AACMgUAAiMFDQABe6yTTsfJ4MY9BA",
    "CAACAgIAAxkBAAEv9VZq2l-rx0u6fV3iZf2H6-LYbbrYHQACTwUAAiMFDQABFxKC9MLEF2A9BA",
    "CAACAgIAAxkBAAEv9Vhq2l_GrU_XxIeFFDcvy5tm3lsavAAChQUAAiMFDQAB8dQJ_lrE9gs9BA",
    "CAACAgIAAxkBAAEv9Vxq2mATVe5mSnBEUVYWdNBixG8ewwACYGEAAjnUKUnt-aCNG0c_Rz0E",
    "CAACAgIAAxkBAAEv9WRq2mAu2lcMVWqoPUBUdXvxnQ19vQADEwAC-nRwS-fHwjGpC730PQQ",
    "CAACAgIAAxkBAAEv9Whq2mBAzWD-wp3o2tkZG5HdxXaafAACFx0AApVVmUugyFQusF-jxz0E",
]

PREDICTIONS = [
    "Сегодня ты будешь невероятно продуктивен. Правда, котик не уточнил, в какой именно вселенной.",
    "Звёзды советуют не принимать важных решений на голодный желудок. Котик подтверждает: сначала поесть.",
    "Сегодня кто-то оценит твои старания. Возможно, кот. Но не будем обесценивать.",
    "Тебя ждёт приятный сюрприз. Проверь доставку: котик чувствует запах упаковки.",
    "Сегодня твоя харизма на высоте. Даже внутренний критик ненадолго отвлечётся на птичку.",
    "День подходит для новых начинаний. Например, начать откладывать дела на завтра.",
    "Сегодня деньги придут к тебе. А потом увидят твой список желаний и уйдут обратно.",
    "Котик предсказывает романтическое настроение. Не путай его с желанием, чтобы тебя никто не трогал.",
    "Сегодня ты услышишь именно то, что хотел. Но, скорее всего, от кофемашины.",
    "Вселенная приготовила тебе знак. Котик тоже приготовил знак, но он на ковре.",
    "Сегодня лучше промолчать в одном споре. Особенно если споришь с котом.",
    "Тебя ждёт важное сообщение. Или рекламная рассылка. Интрига!",
    "Сегодня твой внутренний кот потребует уважения к личным границам. Поддержи его.",
    "Не бойся перемен. Даже кот иногда меняет коробку.",
    "Сегодня удача на твоей стороне. Но кошачья удача работает по собственному графику.",
    "Кто-то думает о тебе. Надеемся, не бухгалтерия.",
    "Сегодня ты можешь изменить чью-то жизнь. Начни с того, чтобы не отвечать «ок» на длинное сообщение.",
    "Котик советует: если проблема решается за пять минут, сначала полежи пять минут.",
    "Сегодня идеальный день, чтобы перестать ждать идеального дня.",
    "Тебе улыбнётся фортуна. Если нет, попробуй улыбнуться первым. Фортуна впечатлительная.",
    "Сегодня не все будут понимать твои решения. Это нормально: коты тоже не понимают, зачем закрывать дверь.",
    "Твой потенциал огромен. Просто сегодня он предпочитает не выходить из-под пледа.",
    "Ожидай маленькую победу. Например, найдёшь вещь, которую сам же положил в надёжное место.",
    "Сегодня лучше не покупать ничего ненужного. Котик уже знает, что ты открыл вкладку магазина.",
    "В любви тебе поможет искренность. А если не поможет — хотя бы сэкономит время.",
    "Сегодня кто-то проверит твоё терпение. Дыши глубже и мысленно урони со стола стакан.",
    "Котик видит перспективу в твоём будущем. Но сначала нужно убрать с него три срочных дела.",
    "Сегодня отличный день для смелого шага. Например, признаться, что ты не понял задачу.",
    "Твоя интуиция сегодня остра, как кошачий коготь. Не игнорируй её, особенно возле сомнительных людей.",
    "Не пытайся контролировать всё. Даже кот не знает, куда исчезла вторая носочная пара.",
    "Сегодня ты будешь особенно убедителен. Главное — не использовать этот дар, чтобы оправдать ещё один десерт.",
    "Вселенная напоминает: ты не обязан быть доступен круглосуточно. Даже служба поддержки иногда спит.",
    "Сегодня кто-то может тебя недооценить. Пусть. Котик тоже не обращает внимания на людей без лакомств.",
    "День благоприятен для финансовых решений. Хотя бы проверь, сколько стоит твоя привычка заказывать кофе.",
    "Сегодня не исключено знакомство с интересным человеком. Или с новым видом сыра. Оба варианта перспективны.",
    "Котик советует не писать бывшим. Если очень хочется — напиши список покупок.",
    "Сегодня у тебя будет шанс блеснуть. Не путай его с блеском экрана в три часа ночи.",
    "Твой сегодняшний суперскилл — делать вид, что всё под контролем. Используй ответственно.",
    "Возможна неожиданная удача. Не задавай лишних вопросов, пока она не передумала.",
    "Сегодня полезно сменить обстановку. Пересесть на другой край дивана тоже считается.",
    "Котик предсказывает: одно маленькое дело принесёт больше облегчения, чем десять часов тревожных размышлений.",
    "Сегодня твои стандарты особенно высоки. Не снижай их ради человека, который пишет «чё делаешь» раз в неделю.",
    "Не принимай чужую срочность за собственную обязанность. Кот не принимает даже собственную срочность.",
    "Сегодня твой главный ресурс — энергия. Распоряжайся ей мудро: не трать всю на людей, которые не умеют читать календарь.",
    "Тебе может повезти в неожиданном месте. Котик рекомендует начать с карманов куртки.",
    "Сегодня ты заслуживаешь комплимент. Если никто не сказал — вот он: ты неплохо справляешься с этой странной жизнью.",
    "Возможен эмоциональный подъём. Не пугайся: это может быть просто хороший кофе.",
    "Сегодня не стоит гнаться за чужим темпом. Даже коты бегают быстро только тогда, когда сами решили.",
    "Котик чувствует: пора избавиться от одной ненужной вещи. Начни с мысли, что ты должен всем нравиться.",
    "Сегодня твои планы могут измениться. Отнесись к этому как кот к упавшей коробке: исследуй и сделай вид, что так и задумано.",
    "В делах поможет любопытство. Но не настолько, чтобы открыть письмо с темой «срочно» в пятницу вечером.",
    "Сегодня будь внимателен к мелочам. Именно там обычно прячутся зарядки, ключи и смысл жизни.",
    "Котик советует не делать выводов по одному сообщению. Особенно если там всего лишь точка.",
    "Сегодня твоя задача — не спасать весь мир. Для начала спаси себя от лишнего созвона.",
    "Кто-то может попросить твоего совета. Дай его честно, а потом не контролируй исполнение. Ты не кот-менеджер.",
    "Сегодня хорошее время для обновления. Начни с настроения, а не с покупки ещё одной вещи.",
    "Твоя привлекательность сегодня повышена. Возможно, дело в уверенности. Возможно, в хорошем освещении.",
    "Котик советует: не сравнивай свой закулисный процесс с чужой витриной. Даже идеальные коты иногда промахиваются мимо коробки.",
    "Сегодня ты можешь найти ответ там, где не искал. Например, в душе, когда наконец перестанешь думать о работе.",
    "Не позволяй одному неловкому моменту испортить весь день. Котик однажды упал с дивана и всё равно считает себя королём.",
    "Сегодня стоит сказать «нет» без диссертации на эту тему.",
    "Тебя ждёт шанс проявить характер. Постарайся, чтобы это было не в переписке с техподдержкой.",
    "Котик чувствует приближение хороших новостей. Если их не будет, новостью станет отсутствие плохих.",
    "Сегодня у тебя есть право передумать. Даже кот может пять минут просить дверь открыть, а потом отказаться выходить.",
    "Не покупай вещь только потому, что у неё красивый сайт. Котик уже проходил эту школу с картонными домиками.",
    "Сегодня кто-то может удивить тебя приятным поступком. Не обесценивай его подозрением, но и розовые очки не надевай.",
    "Котик советует: сначала уточни задачу, потом страдай.",
    "Сегодня удачный день для наведения порядка. Хотя бы в одном чате, где ты уже три года не знаешь половину людей.",
    "Не путай спокойствие со скукой. Иногда лучший сюжет дня — когда никто не пишет «нам надо поговорить».",
    "Сегодня ты можешь оказаться мудрее, чем сам ожидал. Главное — не рассказывать об этом всем подряд.",
    "Котик предупреждает: бесплатное часто оплачивается твоим временем. Подумай, стоит ли оно того.",
    "Сегодня полезно сделать паузу до того, как организм устроит её самостоятельно.",
    "Твоё будущее не требует немедленного ответа. Даже кот не выбирает коробку за одну минуту.",
    "Сегодня не нужно всем нравиться. Даже самый пушистый кот кому-то кажется слишком пушистым.",
    "Котик советует вложиться в то, что действительно улучшает жизнь. Сон, еда и удобная подушка — вполне солидный портфель.",
    "Сегодня возможен маленький повод для гордости. Не жди большой победы, чтобы признать маленькую.",
    "Если что-то не получается с первого раза, попробуй ещё раз. Если это банка с крышкой — попроси кота морально поддержать.",
    "Сегодня не стоит драматизировать задержку ответа. У людей бывают дела, а у котов — внезапная необходимость смотреть в стену.",
    "Котик предсказывает: ты переживёшь этот день и даже найдёшь, над чем посмеяться.",
    "Сегодня хороший момент перестать оправдывать чужое плохое отношение занятостью, стрессом и ретроградным Меркурием.",
    "Твоя удача любит подготовленных. Но иногда приходит к тем, кто просто вышел за хлебом.",
    "Сегодня не обязательно быть лучшей версией себя. Версия, которая поела и ответила на письма, уже достойна уважения.",
    "Котик напоминает: не каждая мысль заслуживает твоего внимания. Некоторые можно просто столкнуть со стола.",
    "Сегодня попробуй сделать что-нибудь ради удовольствия, а не ради результата. Котики строят карьеру именно так.",
    "Возможен неожиданный поворот событий. Сохраняй спокойствие и не выпускай из рук перекус.",
    "Сегодня тебе пригодится чувство юмора. Особенно если кто-то начнёт объяснять очевидное с презентацией на 40 слайдов.",
    "Котик видит в тебе лидера. Но даже лидеру можно делегировать выбор ужина.",
    "Сегодня не нужно заслуживать отдых. Ты не кот на испытательном сроке.",
    "Если день идёт не по плану, составь новый. Котик вообще не пользуется календарём и выглядит вполне счастливым.",
    "Сегодня будь добр к себе. Ты уже достаточно раз пережил ситуации, которые когда-то казались концом света.",
    "Котик предсказывает хороший финал дня: что-то вкусное, немного тишины и ни одного обязательного разговора.",
    "Сегодня твой девиз: меньше суеты, больше достоинства. Как у кота, который уронил вазу и ждёт извинений.",
    "Самое важное предсказание дня: ты не обязан решить всю жизнь сегодня. Даже у кота девять жизней, а он всё равно спит.",
    "Сегодня котик советует выбрать мир вместо правоты. Но если спор о том, кто красивее, уступать не обязательно.",
    "Не откладывай радость на выходные. Котик радуется уже тому, что коробка приехала.",
    "Сегодня кто-то оценит твою честность. А если нет — хотя бы котик поставит мысленную лапку вверх.",
    "Твоя задача дня — не отвечать на каждую тревожную мысль. Некоторые мысли просто пришли поглазеть.",
    "Котик предсказывает удачный момент для прогулки, вкусного обеда или драматичного взгляда в окно.",
    "Сегодня избегай решений из чувства вины. Даже кот не извиняется за то, что занял твоё место.",
    "Помни: ты можешь быть амбициозным и всё равно лечь пораньше. Котик называет это стратегией."
]

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("participants", [])
            data.setdefault("history", {})
            data.setdefault("stats", {})
            return data
    except FileNotFoundError:
        return {"participants": [], "history": {}, "stats": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def backup_to_github():
    try:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("No GitHub token found")
            return
        repo_url = f"https://{token}@github.com/arestova/kotik-bot.git"
        subprocess.run(["git", "config", "--global", "user.email", "bot@kotik.local"])
        subprocess.run(["git", "config", "--global", "user.name", "Kotik Bot"])
        subprocess.run(["git", "add", "data.json"])
        subprocess.run(["git", "commit", "-m", "Auto update kotik stats"], check=False)
        result = subprocess.run(["git", "push", repo_url, "main"], check=False)
        if result.returncode == 0:
            print("Backup to GitHub successful")
        else:
            print("Backup to GitHub failed; push returned non-zero status")
    except Exception as e:
        print(f"GitHub backup failed: {e}")


def format_mention(user):
    if user.get("username"):
        return f"@{user['username']}"
    return user.get("name", "Unknown")


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
        backup_to_github()
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

    if today in data["history"]:
        record = data["history"][today]
        winner = record["winner"]
        sticker = record.get("sticker")
        prediction = record.get("prediction")

        # Если сегодняшний результат был сохранён до добавления прогнозов,
        # добавляем прогноз к существующей записи, не меняя победителя,
        # стикер или статистику.
        if not prediction and PREDICTIONS:
            prediction = random.choice(PREDICTIONS)
            record["prediction"] = prediction
            data["history"][today] = record
            save_data(data)
            backup_to_github()

        mention = format_mention(winner)

        if sticker:
            await update.message.reply_sticker(sticker)
        await update.message.reply_text(
            f"🐱 Сегодняшний котик дня уже выбран — {mention}!"
        )
        if prediction:
            await update.message.reply_text(f"🔮 Прогноз котика:\n{prediction}")
        return

    winner = random.choice(participants)
    sticker = random.choice(STICKERS) if STICKERS else None
    prediction = random.choice(PREDICTIONS) if PREDICTIONS else None

    data["history"][today] = {
        "winner": winner,
        "sticker": sticker,
        "prediction": prediction,
    }

    user_id = str(winner["id"])
    data["stats"][user_id] = data["stats"].get(user_id, 0) + 1
    save_data(data)
    backup_to_github()

    mention = format_mention(winner)
    if sticker:
        await update.message.reply_sticker(sticker)
    await update.message.reply_text(f"🐱 Сегодня котик дня — {mention}!")
    if prediction:
        await update.message.reply_text(f"🔮 Прогноз котика:\n{prediction}")


async def kotik_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    participants = data.get("participants", [])
    stats = data.get("stats", {})

    if not participants:
        await update.message.reply_text(
            "Пока нет зарегистрированных участников."
        )
        return

    full_stats = []
    for participant in participants:
        user_id = str(participant["id"])
        wins = stats.get(user_id, 0)
        display_name = (
            participant.get("username")
            if participant.get("username")
            else participant.get("name", "Unknown")
        )
        full_stats.append((display_name, wins))

    full_stats.sort(key=lambda x: x[1], reverse=True)
    text = "📊 Статистика котиков дня:\n\n"
    for name, wins in full_stats:
        text += f"{name} — {wins} 🐱\n"
    await update.message.reply_text(text)


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kotik_of_the_day", kotik_of_the_day))
    app.add_handler(CommandHandler("kotik_stats", kotik_stats))
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
