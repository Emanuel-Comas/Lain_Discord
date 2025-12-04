import time
import re

## Expresión regular para detectar URLs en un mensaje.
URL_REGEX = r"(https?://[^\s]+)"


class LainIDS:

    def __init__(self, owner_id: int, ignored=None, config=None, suspicious_domains=None):
        self.owner_id = owner_id
        ## agrega automáticamente tu OWNER_ID a la lista de ignorados, independientemente de lo que pongas en 
        # 'ignored_users' en 'config.json'.
        self.ignored = set(ignored or [])
        # Esta linea se puede comentar para hacer pruebas, ya que sino Lain te ignora al ser admin.
        self.ignored.add(owner_id)

        # Última alerta enviada por usuario y tipo
        self.last_alert = {}  # { user_id: { "delete": timestamp, "flood": timestamp, ... } }

        # Cooldown en segundos (puede ser ajustable)
        self.ALERT_COOLDOWN = 60  # 60 segundos

        # Thresholds cargados desde config.json
        ## Límites de eventos cargados desde config.json
        self.MSG_FLOOD_LIMIT = config.get("msg_flood_limit", 6)
        self.MSG_FLOOD_SECONDS = config.get("msg_flood_seconds", 5)

        self.EDIT_LIMIT = config.get("edit_limit", 5)
        self.DELETE_LIMIT = config.get("delete_limit", 6)

        self.SPAM_REPEAT_LIMIT = config.get("spam_repeat_limit", 3)
        self.NEW_ACCOUNT_DAYS = config.get("new_account_days", 7)

        # Lista de dominios sospechosos
        self.suspicious_domains = suspicious_domains or []

        # Memoria de eventos
        self.msg_history = {}
        self.edit_history = {}
        self.delete_history = {}
        self.repeat_count = {}
        self.last_messages = {}

    # --------------------------------------------------------------

    ## Revisa si el mensaje contiene URLs de la lista de dominios sospechosos.
    ## Devuelve un string con la alerta o None si no hay nada.

    def check_suspicious_url(self, msg):
        content = msg.content
        found = re.findall(URL_REGEX, content)
        if not found:
            return None

        for url in found:
            for domain in self.suspicious_domains:
                if domain.lower() in url.lower():
                    return f"URL sospechosa detectada: `{url}`"

        return None

    # --------------------------------------------------------------

    ## Detecta flood: si un usuario envía demasiados mensajes en un corto periodo.
    def check_flood(self, user_id):
        now = time.time()
        history = self.msg_history.setdefault(user_id, [])
        history.append(now)

        # Recorta eventos viejos
        ## Limita la memoria a los últimos MSG_FLOOD_SECONDS
        history = [t for t in history if now - t <= self.MSG_FLOOD_SECONDS]
        self.msg_history[user_id] = history

        if len(history) >= self.MSG_FLOOD_LIMIT:
            return "Posible flood de mensajes."
        return None

    # --------------------------------------------------------------

    ## Detecta si un usuario repite el mismo mensaje varias veces.
    def check_repeated(self, user_id, content):
        last = self.last_messages.get(user_id)
        if last == content:
            self.repeat_count[user_id] = self.repeat_count.get(user_id, 1) + 1
        else:
            self.repeat_count[user_id] = 1

        self.last_messages[user_id] = content

        if self.repeat_count[user_id] >= self.SPAM_REPEAT_LIMIT:
            return "Repetición excesiva del mismo mensaje."
        return None

    # --------------------------------------------------------------

    ## Detecta ediciones excesivas de mensajes.
    def check_edit(self, user_id):
        now = time.time()
        hist = self.edit_history.setdefault(user_id, [])
        hist.append(now)

        ## Solo consideramos las ediciones recientes (6 segundos)
        hist = [t for t in hist if now - t <= 6]
        self.edit_history[user_id] = hist

        if len(hist) >= self.EDIT_LIMIT:
            return "Ediciones excesivas."
        return None

    # --------------------------------------------------------------

    ## Detecta borrados excesivos de mensajes.
    def check_delete(self, user_id):
        now = time.time()
        hist = self.delete_history.setdefault(user_id, [])
        hist.append(now)

        ## Solo consideramos borrados recientes (6 segundos)
        hist = [t for t in hist if now - t <= 6]
        self.delete_history[user_id] = hist

        if len(hist) >= self.DELETE_LIMIT:
            return "Borrados excesivos."
        return None

    # --------------------------------------------------------------

    # Detectores principales ----------------------------------------


    """
        Detecta alertas sobre mensajes nuevos:
        - URLs sospechosas
        - Flood
        - Mensajes repetidos
        Devuelve alerta o None, respetando cooldown.
    """
    def detect_message(self, message):
        user = message.author

        if user.bot or user.id in self.ignored:
            return None

        # URLs sospechosas
        url_alert = self.check_suspicious_url(message)
        if url_alert and self.can_alert(user.id, "url"):
            return url_alert

        # Flood
        flood_alert = self.check_flood(user.id)
        if flood_alert and self.can_alert(user.id, "flood"):
            return flood_alert

        # Mensaje repetido
        rep_alert = self.check_repeated(user.id, message.content)
        if rep_alert and self.can_alert(user.id, "repeat"):
            return rep_alert

        return None

    ## Detecta alertas sobre mensajes editados.
    def detect_edit(self, before, after):
        user = after.author
        if user.bot or user.id in self.ignored:
            return None

        alert = self.check_edit(user.id)
        if alert and self.can_alert(user.id, "edit"):
            return alert

    ## Detecta alertas sobre mensajes borrados.
    def detect_delete(self, message):
        user = message.author
        if user.bot or user.id in self.ignored:
            return None

        alert = self.check_delete(user.id)
        if alert and self.can_alert(user.id, "delete"):
            return alert
        return None
    
    ## Función auxiliar para controlar cooldown de alertas.
    """
        Controla el cooldown de alertas por usuario y tipo.
        Evita enviar alertas repetidas constantemente.
        Devuelve True si se puede enviar alerta, False si está en cooldown.
    """
    def can_alert(self, user_id, alert_type):
        import time
        now = time.time()
        if user_id not in self.last_alert:
            self.last_alert[user_id] = {}
        last = self.last_alert[user_id].get(alert_type, 0)
        if now - last < self.ALERT_COOLDOWN:
            return False  # todavía en cooldown
        self.last_alert[user_id][alert_type] = now
        return True
