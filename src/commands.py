from discord.ext import commands
import asyncio
import psutil
from discord import Embed
from src.status import status_list
from src.glitch import glitch

def setup_commands(bot):

    @bot.command()
    # El nombre del comando en discord, es por defecto el nombre de función, aqui es "hola",
    # Es decir: async def hola():
    async def hola(ctx):
        """Saludo de Lain"""
        # O ctx.author.name, o ctx.author.mention
        usuario = ctx.author.display_name
        await ctx.send(f"Hola… {ctx.author.display_name}. La WIRED te observa.")

    @bot.command()
    async def status_lain(ctx):
        """Muestra el uso actual de CPU y RAM del sistema."""
        # Esto no mide solo Lain, sino todo el sistema.
        # Todos los procesos de la máquina cuentan.
        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        await ctx.send(
            f"💻 Uso de recursos:\nCPU: {cpu}%\nRAM: {ram.percent}% ({ram.used // (1024**2)}MB / {ram.total // (1024**2)}MB)"
        )

    @bot.command()
    async def recordar(ctx, tiempo:int, *, mensaje):
        """Te envía un recordatorio en DM después de la cantidad de segundos indicada."""
        await ctx.send(f"Ok, te recordaré en {tiempo} segundos.")
        await asyncio.sleep(tiempo)
        await ctx.author.send(f"⏰ Recordatorio: {mensaje}")

    @bot.command()
    async def glitch_text(ctx, *, texto):
        """Aplica un efecto de texto glitch y lo muestra en el chat."""
        await ctx.send(glitch(texto, intensidad=2, legible=True))

    @bot.command(name="help_lain")
    async def help_lain(ctx, *, comando=None):
        """Muestra la lista de comandos o detalles de un comando específico"""
        if comando:
            cmd = bot.get_command(comando)
            if cmd:
                await ctx.send(f"**{cmd.name}**: {cmd.help or 'Sin descripción'}")
            else:
                await ctx.send(f"No se encontró el comando `{comando}`")
        else:
            help_msg = "**Comandos disponibles:**\n"
            for cmd in bot.commands:
                help_msg += f"- {cmd.name}: {cmd.help or 'Sin descripción'}\n"
            help_msg += "\nUsa `!help_lain <comando>` para más información."
            await ctx.send(help_msg)

    @bot.command()
    async def decir(ctx, usuario: commands.MemberConverter, *, mensaje):
        """Envía un mensaje estilizado al DM del usuario y borra el comando del canal."""
    
        # Borrar el mensaje del canal
        try:
            await ctx.message.delete()
        except:
            pass

        # Agrega prefijo >> al mensaje sin glitch
        mensaje_formateado = f">> {mensaje}"

        # Crear embed estilo Lain
        embed = Embed(
            title="📡 Mensaje entrante desde la WIRED",
            description=f"```\n{mensaje_formateado}\n```",
            color=0x9b59b6
        )
        embed.set_footer(text=f"Transmitido por {ctx.author.display_name}")

        # Intentar enviar DM
        try:
            await usuario.send(embed=embed)
        except:
            await ctx.send("No puedo enviarle DMs a ese usuario.", delete_after=5)




