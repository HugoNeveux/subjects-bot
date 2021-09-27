from discord.ext import commands, tasks
from discord.utils import get
import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Load bot config
with open("config.yml") as configfile:
    config = yaml.safe_load(configfile)
    TOKEN = config["token"]
    SUBJECTS_CHANNEL = config["channel"]
    PING_ROLE = config["ping_role_id"]

bot = commands.Bot("$")

async def send_daily_subject():
    """
    This functions sends a message every day in SUBJECTS_CHANNEL
    """
    channel = bot.get_channel(SUBJECTS_CHANNEL) # Get channel object
    with open("daily_subjects.txt", "r") as daily_subjects_list:
        subjects = daily_subjects_list.read().split("\n")
    try:
        await channel.send(f"<&{PING_ROLE}> Bonjour ! Le sujet est {subjects[0]}")   # Send subject
    except IndexError:
        await channel.send("Il n'y a pas de sujet prévu pour aujourd'hui.")
        return
    subjects = subjects[1:]
    with open("daily_subjects.txt", "w") as daily_subjects_list:
        daily_subjects_list.write("\n".join(subjects))  # Edit subjects list

@bot.event
async def on_ready():
    """
    Function executed when the bot is running
    """
    print("Bot ready, configuration loaded.")
    print(f"Subjects channel : {SUBJECTS_CHANNEL}")
    print(f"Ping role : {PING_ROLE}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_subject, CronTrigger.from_crontab("0 0 * * *"))
    scheduler.start()

bot.run(TOKEN, bot=True, reconnect=True)
