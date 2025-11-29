import os
from .glitch import glitch
import logging
from datetime import datetime
from dotenv import load_dotenv
import discord

load_dotenv()

OWNER_ID = int(os.getenv("OWNER_ID"))

os.makedirs("logs", exist_ok=True)

# Crea (o recupera) un logger llamado "server_activity".
server_logger = logging.getLogger("server_activity")
# Le dice al logger que guarde los mensajes en un archivo llamado logs/server_activity.log.
handler = logging.FileHandler("logs/server_activity.log")
# Define el formato de los logs, aquí guarda la fecha y hora y luego el mensaje.
formatter = logging.Formatter("%(asctime)s | %(message)s")
# Asocia el formato al handler (archivo).
handler.setFormatter(formatter)
# Agrega el handler al logger, es decir, que los logs se escriban en el archivo.
server_logger.addHandler(handler)
# Define el nivel mínimo de mensajes que se guardarán (INFO y superior).
server_logger.setLevel(logging.INFO)


async def protection_event(bot, message):
    print(f"Debug mensaje recibido de {message.author}: {message.content}")
    # Se ignroa cualquier bot, incluida Lain.
    if message.author.bot:
        return

    # Si mencionan al usuario admin (tú)
    if any(user.id == OWNER_ID for user in message.mentions):

        autor = message.author.display_name
        contenido = message.content

        # 1) Lain responde en el canal
        texto = "Obito está protegido… no interfieras con su señal."
        await message.channel.send(glitch(texto, intensidad=3))

        owner = bot.get_user(OWNER_ID)
        if owner is None:
            owner = await bot.fetch_user(OWNER_ID)

        try:
            await owner.send(
                f"⚠️ Te mencionaron en un servidor.\n"
                f"👤 Autor: **{autor}**\n"
                f"💬 Mensaje: {contenido}\n"
                f"⏰ Hora: {datetime.now()}"
            )
        except discord.Forbidden:
            print("No se pudo enviar DM al owner (privacidad activada).")

        
