# src/auto_msgs.py
import asyncio
import random
import os
from src.glitch import glitch
from dotenv import load_dotenv

load_dotenv()  # cargar variables del .env

# ID del canal tomado desde el .env
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Lista de mensajes automáticos de Lain
mensajes = [
    "Escuchando señales residuales...",
    "Conectada a la WIRED...",
    "Fragmentos de información detectados...",
    "Observando la red…",
    "Señales inusuales detectadas…"
]

async def start_auto_messages(bot):
    canal = bot.get_channel(CHANNEL_ID)
    if not canal:
        print("No se encontró el canal para mensajes automáticos.")
        return

    while True:
        mensaje = random.choice(mensajes)
        # Enviar mensaje con glitch suave y legible
        await canal.send(glitch(mensaje, intensidad=1, legible=True))
        await asyncio.sleep(60)  # esperar 60 segundos antes del siguiente
