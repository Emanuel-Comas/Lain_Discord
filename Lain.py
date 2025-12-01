import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
from src.protection import server_logger
from src.ids import LainIDS
import json

from src.status import start_status_task
from src.auto_msgs import start_auto_messages
from src.protection import protection_event
from src.commands import setup_commands

load_dotenv()
OWNER_ID = int(os.getenv("OWNER_ID"))

# carpeta donde está Lain.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
config_path = os.path.join(BASE_DIR, "src", "config", "config.json")

## Lerctura archivo config.json
with open(config_path, "r") as f:
        CONFIG = json.load(f)


## Creacion de carpeta logs y configuración logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/lain.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


## Iniciar a Lain.

intents = discord.Intents.default()
# necesario para leer contenido de mensajes.
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

## Inicializar IDS antes de on_ready
bot.ids = LainIDS(
    owner_id=OWNER_ID,
    ignored=CONFIG["ignored_users"],
    config=CONFIG["ids"],
    suspicious_domains=CONFIG["suspicious_domains"]
    )


# ------------------------------
# Función auxiliar para enviar alertas al owner con embed
# ------------------------------
async def send_ids_alert(bot, alert_type, message=None, before=None, after=None):
    """Envía un embed al OWNER_ID con la alerta del IDS."""
    owner = await bot.fetch_user(OWNER_ID)
    
    embed = discord.Embed(
        title=f"[IDS ALERT] {alert_type}",
        color=discord.Color.red(),
        timestamp=discord.utils.utcnow()  # Vuelve a la normalidad
    )
    
    if message:
        embed.add_field(name="Usuario", value=message.author, inline=True)
        embed.add_field(name="Contenido", value=message.content or "N/A", inline=False)
    elif before and after:
        embed.add_field(name="Usuario", value=after.author, inline=True)
        embed.add_field(name="Antes", value=before.content or "N/A", inline=False)
        embed.add_field(name="Después", value=after.content or "N/A", inline=False)
    
    embed.set_footer(text=f"Tipo de alerta: {alert_type}")
    
    try:
        await owner.send(embed=embed)
    except discord.Forbidden:
        print("No se pudo enviar DM al owner (privacidad activada).")




## Se ejecuta cuando Lain se conecta a discord.
@bot.event
async def on_ready():
    print("Lain está conectada a la WIRED.")
    # Cambia estado en barra de Discord
    start_status_task(bot)
    logging.info("Lain se ha conectado correctamente a la WIRED.")


## Eventos on_message (único).
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
     # Protección personal
    await protection_event(bot, message)

    # IDS: analizar mensaje
    alerta = bot.ids.detect_message(message)
    if alerta:
        owner = await bot.fetch_user(OWNER_ID)
        await send_ids_alert(bot, alerta, message=message)
    ## Va al final, sino no funcionan los comandos.
    ## Procesar comandos al final.
    await bot.process_commands(message)



## Eventos de edición y borrado

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    # Log del mensaje borrado
    server_logger.info(f"Mensaje eliminado: {message.author} dijo: {message.content}")

    # IDS delete
    alerta = bot.ids.detect_delete(message)
    if alerta:
        owner = await bot.fetch_user(OWNER_ID)
        await send_ids_alert(bot, alerta, message=message)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return

    # Log del mensaje editado
    server_logger.info(f"Mensaje editado: {before.author} de '{before.content}' a '{after.content}'")

    # IDS edit
    alerta = bot.ids.detect_edit(before, after)
    if alerta:
        owner = await bot.fetch_user(OWNER_ID)
        await send_ids_alert(bot, alerta, before=before, after=after)


## Configuración de comandos
setup_commands(bot)



## Manejo de errores de comandos

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No reconozco ese comando… ¿quizás te equivocaste?")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permiso para eso…")
    else:
        # Opcional: loguear errores más graves en consola
        print(f"Ocurrió un error: {error}")


## Ejecutar a Lain.
bot.run(os.getenv("DISCORD_TOKEN"))
