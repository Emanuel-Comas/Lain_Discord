# Lain Discord Bot

    Lain es un bot de Discord inspirado en *Serial Experiments Lain*. Su objetivo principal es **proteger al usuario Admin en el servidor**, enviar mensajes automáticos con estilo hacker/glitch, y ofrecer funcionalidades adicionales como recordatorios y monitorización.

---

## 🗂 Estructura de carpetas

```
Lain_Discord/
│
├─ bot.py                   # Archivo principal del bot
├─ .env                     # Variables de entorno
├─ logs/                    # Carpeta donde se guardan los logs
    ├─ lain.log
    ├─ server_activity.log
└─ src/
    ├─ status.py           # Cambia el estado de Lain en la barra del bot
    ├─ auto_msgs.py        # Mensajes automáticos con estilo glitch (Sin uso actualmente)
    ├─ protection.py       # Protección de Obito y advertencias en DM
    ├─ glitch.py           # Función de 'glitch' para textos
    └─ commands.py         # Definición de comandos
```

---

## ⚙ Instalación

1. Clona o descarga el repositorio.  
2. Crea un entorno virtual y actívalo:

```bash
python -m venv venv
# Windows, iniciar entorno
venv\Scripts\activate
# Salir de entorno
deactivate
# macOS / Linux
source venv/bin/activate
# Salir de entorno
deactivate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

> `requirements.txt` debería incluir al menos:
> ```
> discord.py==2.6.4
> python-dotenv
> psutil
> ```

4. Configura tu archivo `.env` con tus credenciales:

```
DISCORD_TOKEN=tu_token_aqui
DISCORD_CHANNEL_ID=123456789012345678
OWNER_ID=tu_id_de_discord
```

- `DISCORD_TOKEN` → token de tu bot en Discord Developer Portal  
- `DISCORD_CHANNEL_ID` → ID del canal donde Lain enviará mensajes automáticos  
- `OWNER_ID` → tu ID de Discord para recibir advertencias por DM

5. Ejecuta el bot:

```bash
python Lain.py
```

---

## 📝 Funcionalidades actuales

### Estado del bot

    - Lain cambia automáticamente su **estado en la barra de bots** cada cierto tiempo con frases estilo hacker/glitch.  
    - Este cambio **no envía mensajes** al canal.

### Mensajes automáticos

    - Lain envía mensajes periodicos a un canal definido (DISCORD_CHANNEL_ID).  
    - Texto con estilo legible y glitch opcional.
    - Intervalos configurables.

### Protección y advertencias

    - Si alguien menciona al "UserAdmin" o intenta interactuar directamente, Lain enviará **un DM al OWNER_ID** con:
    - Fecha y hora
    - Nombre de usuario
    - Contenido del mensaje
    - Esto funciona incluso si el mensaje es borrado después.

### Comandos implementados

Actualmente disponibles:

- **`!hola`** → Lain responde con un saludo hacker/glitch:  
  ```
  Hola… Obito. La WIRED te observa.
  
    -- Obito => Mi userName en discord, es usado asi para evitar que hable diciendo tu ID de discord,
    quedaria menos bonito, se lo puede cambiar a otro userName y ya.
  
  ```

- **`!recordar <tiempo_en_segundos> <mensaje>`** → Lain envía un recordatorio por DM al usuario que lo solicitó:  
  ```
    !recordar 60 Tomar agua
    ⏰ Recordatorio: Tomar agua
  ```

- **`!status_lain`** → Muestra el estado actual del bot y uso de recursos (CPU/RAM).

- **`!glitch_text <texto>`** → Convierte el texto proporcionado en estilo glitch legible.

- **`!decir <User> <texto>`** → Envia un mensaje privado al usuario elegido con el mensaje que quieras.

---

## 📂 Módulos del bot

### `Lain.py`

    - Archivo principal que inicializa el bot, carga `.env` y los módulos del bot.  
    - Controla los eventos `on_ready`, `on_message` y `on_command_error`.  
    - Ejecuta las tareas de **mensajes automáticos** y **cambio de estado**.

### `src/status.py`

    - Contiene la función `start_status_task(bot)` que cambia el **estado de Lain** en la barra del bot.  
    - No envía mensajes en el canal.

### `src/auto_msgs.py`

    - Contiene `start_auto_messages(bot)` que envía mensajes automáticos con efecto **glitch**.  
    - Los mensajes se envían en el canal definido por `DISCORD_CHANNEL_ID` en `.env`.  
    - La frecuencia y los textos pueden personalizarse.

### `src/protection.py`

    - Contiene `protection_event(bot, message)` que protege al usuario Obito.  
    - Envía **DM al OWNER_ID** con fecha, hora, usuario y contenido si alguien menciona a Obito.  
    - Funciona incluso si el mensaje es borrado.

### `src/commands.py`

    - Contiene los comandos definidos:

        1. `!hola` → saludo estilo Lain.  
        2. `!recordar <tiempo_en_segundos> <mensaje>` → recordatorio por DM.  
        3. `!status_bot` → muestra CPU/RAM y estado del bot.  
        4. `!glitch_text <texto>` → convierte texto en glitch legible.

### `src/glitch.py`

    - Función auxiliar para aplicar efecto 'glitch' a los textos:

        -- Usada en:

            -- Mensajes automáticos
            -- Portección de menciónes
            -- Comando !glitch_text

### `logs/`

    - `lain.log` => Registra eventos generales del bot, como conexón y errores de comandos.
    - `server_activity.log` => Registra mensajes eliminados, editados y menciones del OWNER_ID.

---

### IDS (Intrusion Detection System)

    config.json:

        ignored_users": [] => El OWNER se agrega automaticamente.

            -- Es para decirle al IDS que ciertos usuarios no deben generar alertas.

            Ejemplo:

                "ignored_users": [123456789012345678, 987654321098765432]

    Mantiene las alertas para:

        -- Mensajes sospechosos:

            URLs o dominios peligrosos configurados en 'config.json', son analizados; si coinciden con la lista de suspicious_domains, se genera una alerta al OWNER.

        -- Mensajes editados/eliminados:

            La alerta sigue funcionando incluso si el mensaje se borra o se edita.

        Las alertas se envían en embed al propietario con información detallada: usuario, contenido antes/después, tipo de alerta.

        -- Mejora en embeds de alertas:

            Los embeds ahora tienen:

            Footer indicando el tipo de alerta

            Estructura clara y visual para autor, contenido y hora

            Facilita revisar rápidamente los eventos importantes.

        -- Logging → Todos los eventos relevantes se registran en logs/server_activity.log para revisión.

## 🔧 Notas adicionales

    - Todos los textos de Lain, mensajes automáticos y efectos glitch pueden personalizarse en los archivos correspondientes.  
    - La protección en DM y los recordatorios son **solo visibles para el OWNER_ID**.  
    - El bot no tiene permisos de administración sobre los usuarios, por seguridad.
