import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
from src.protection import server_logger

load_dotenv()

from src.status import start_status_task
from src.auto_msgs import start_auto_messages
from src.protection import protection_event
from src.commands import setup_commands

intents = discord.Intents.default()
intents.message_content = True  # necesario

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/lain.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Lain está conectada a la WIRED.")
    start_status_task(bot)
    logging.info("Lain se ha conectado correctamente a la WIRED.")

@bot.event
async def on_message(message):
    await protection_event(bot, message)
    await bot.process_commands(message)

setup_commands(bot)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No reconozco ese comando… ¿quizás te equivocaste?")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permiso para eso…")
    else:
        # Opcional: loguear errores más graves en consola
        print(f"Ocurrió un error: {error}")


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    server_logger.info(f"Mensaje eliminado: {message.author} dijo: {message.content}")

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    server_logger.info(f"Mensaje editado: {before.author} de '{before.content}' a '{after.content}'")


bot.run(os.getenv("DISCORD_TOKEN"))
