from discord.ext import commands
import asyncio
import psutil
from discord import Embed
from src.modules.status import status_list
from src.modules.glitch import glitch

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

    # Define un comando llamado "help_lain" en Discord.
    @bot.command(name="help_lain")
    # Función del comando
    # ctx = información del mensaje (usuario, canal, etc).
    # comando = texto opcional después del comando (!help_lain hola).
    async def help_lain(ctx, *, comando=None):

        # Si el usuario escribió algo después de !help_lain (ej: !help_lain hola).
        if comando:
            # Busca si existe un comando con ese nombre.
            cmd = bot.get_command(comando)
            # Si el comando existe
            if cmd:
                # Envía un mensaje con estilo "fix" (tipo consola).
                # Muestra:
                # - nombre del comando.
                # - descripción del comando (o texto por defecto si no hay).
                await ctx.send(f"""```fix
    >> COMMAND TRACE
    !{cmd.name}
    {cmd.help or 'no description'}
    ```""")
            # Si no existe el comando
            else:
                # Envía mensaje estilo error (rojo en Discord)
                # Muestra error diciendo que no existe
                await ctx.send(f"""```diff
    - ERROR: command '!{comando}' not found
    ```""")
            # Termina la función aquí si se buscó un comando específico
            return

        # Si NO se escribió ningún comando, muestra la ayuda general
        await ctx.send("""```yaml
    ┌──────────────────────────────┐
    │   🟣 LAIN WIRED INTERFACE    │
    └──────────────────────────────┘

    [ SYSTEM COMMANDS ]

    🟢 !help        → Standard help interface
    🟢 !help_lain   → Command info system
    🟢 !status_lain → System CPU / RAM status

    [ USER INTERACTION ]

    🟡 !hola        → Lain greeting protocol
    🟡 !decir       → Sends a private message to the selected user
    🟡 !recordar    → Timed reminder

    [ EFFECTS ]

    🟣 !glitch_text → Glitch text renderer

    ──────────────────────────────
    >> ACCESS LEVEL: SYSTEM ADMINISTRATOR
    >> USE: !help_lain <command>
    ```""")
    # '>> ACCESS LEVEL: SYSTEM ADMINISTRATOR' => Nivel de acceso mostrado (solo estética).
    # >> USE: !help_lain <command> => Instrucción de uso.

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




