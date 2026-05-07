from discord.ext import tasks
import discord
import random

status_list = [
    "conectada a la WIRED…",
    "escuchando señales residuales…",
    "procesando fragmentos de información…"
]

def start_status_task(bot):
    @tasks.loop(seconds=40)
    async def cambiar_status():
        # SOLO cambia la presencia/estado de Lain, nada más.
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=random.choice(status_list)
            )
        )

    cambiar_status.start()
