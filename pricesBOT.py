import requests
import time
from datetime import datetime
from flask import Flask
from threading import Thread
import pytz
import os  # Para variables de entorno
from dotenv import load_dotenv  # Para cargar .env

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
tokens = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ronin": "RON",
    "solana": "SOL",
    "binancecoin": "BNB",
    "banana": "BANANA",
    "axie-infinity": "AXS"
}
precios_anteriores = {token: None for token in tokens}
intervalo = 60
telegram_token = os.getenv("TELEGRAM_TOKEN")  # Token desde variable de entorno
chat_ids = {}

PAIS_A_ZONA = {
    "argentina": "America/Argentina/Buenos_Aires",
    "spain": "Europe/Madrid",
    "usa": "America/New_York",
    "uk": "Europe/London",
    "brazil": "America/Sao_Paulo",
    "france": "Europe/Paris",
    "germany": "Europe/Berlin",
    "italy": "Europe/Rome",
}

def obtener_precios():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(tokens.keys()), "vs_currencies": "usd"}
    respuesta = requests.get(url, params=params)
    return respuesta.json()

def calcular_cambio(precio_anterior, precio_actual):
    if precio_anterior is None:
        return 0
    cambio = ((precio_actual - precio_anterior) / precio_anterior) * 100
    return cambio

def notificar(precios, cambios):
    mensaje_base = "<b>📊 Actualización de Precios 📊</b>\n"
    emoji_token = {
        "bitcoin": "₿",
        "ethereum": "Ξ",
        "ronin": "🎮",
        "solana": "◎",
        "binancecoin": "💰",
        "banana": "🍌",
        "axie-infinity": "🎮"
    }
    for token in tokens:
        precio_actual = precios[token]["usd"]
        cambio = cambios[token]
        simbolo = "⬆️" if cambio > 0 else "⬇️" if cambio < 0 else "➡️"
        mensaje_base += (
            f"{tokens[token]} {emoji_token.get(token, '💸')}: <b>${precio_actual:,.2f}</b> | "
            f"{cambio:.2f}% {simbolo}\n"
            f"{'-' * 20}\n"
        )
    for chat_id, timezone in chat_ids.items():
        tz = pytz.timezone(timezone)
        hora_local = datetime.now(pytz.utc).astimezone(tz)
        mensaje = mensaje_base + f"Hora local: {hora_local.strftime('%H:%M:%S')} ({timezone})"
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": mensaje,
            "parse_mode": "HTML"
        }
        respuesta = requests.get(url, params=params)
        print(f"Enviado a {chat_id}: OK={respuesta.ok}, Status={respuesta.status_code}")

def manejar_updates():
    ultimo_update_id = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/getUpdates"
            if ultimo_update_id:
                url += f"?offset={ultimo_update_id + 1}"
            respuesta = requests.get(url, timeout=10).json()
            if respuesta["ok"] and respuesta["result"]:
                for update in respuesta["result"]:
                    ultimo_update_id = update["update_id"]
                    if "message" in update and "text" in update["message"]:
                        chat_id = str(update["message"]["chat"]["id"])
                        texto = update["message"]["text"]
                        if texto == "/start" and chat_id not in chat_ids:
                            chat_ids[chat_id] = "UTC"
                            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                            params = {
                                "chat_id": chat_id,
                                "text": (
                                    "¡Te has suscrito! Recibirás precios cada minuto.\n"
                                    "Por favor, configura tu país con:\n"
                                    "/setcountry <país>\n"
                                    "Ejemplos: /setcountry Argentina, /setcountry Spain"
                                )
                            }
                            requests.get(url, params=params)
                            print(f"Nuevo usuario suscrito: {chat_id} con UTC")
                        elif texto.startswith("/setcountry "):
                            pais = texto.split(" ", 1)[1].strip().lower()
                            if pais in PAIS_A_ZONA:
                                zona = PAIS_A_ZONA[pais]
                                chat_ids[chat_id] = zona
                                tz = pytz.timezone(zona)
                                hora_local = datetime.now(pytz.utc).astimezone(tz)
                                url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                                params = {
                                    "chat_id": chat_id,
                                    "text": f"País configurado a {pais.capitalize()}. Hora local ahora: {hora_local.strftime('%H:%M:%S')} ({zona})"
                                }
                                requests.get(url, params=params)
                                print(f"Zona horaria de {chat_id} cambiada a {zona}")
                            else:
                                url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
                                params = {
                                    "chat_id": chat_id,
                                    "text": (
                                        "País no reconocido. Usa nombres como:\n"
                                        "Argentina, Spain, USA, UK, Brazil, France, Germany, Italy\n"
                                        "Ejemplo: /setcountry Argentina"
                                    )
                                }
                                requests.get(url, params=params)
        except Exception as e:
            print(f"Error en manejar_updates: {e}")
        time.sleep(5)

@app.route('/api/prices')
def get_all_prices():
    precios = obtener_precios()
    return precios

@app.route('/api/token/<token_id>')
def get_token_price(token_id):
    if token_id not in tokens:
        return {"error": "Token no encontrado"}, 404
    precios = obtener_precios()
    return {token_id: precios[token_id]}

@app.route('/')
def home():
    return "Bot corriendo!"

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_bot():
    while True:
        precios = obtener_precios()
        cambios = {}
        for token in tokens:
            precio_actual = precios[token]["usd"]
            cambios[token] = calcular_cambio(precios_anteriores[token], precio_actual)
            precios_anteriores[token] = precio_actual
        notificar(precios, cambios)
        print(f"Chequeo a las {datetime.now().strftime('%H:%M:%S')} UTC - Esperando 1 min...")
        time.sleep(intervalo)

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    bot_thread = Thread(target=run_bot)
    updates_thread = Thread(target=manejar_updates)
    flask_thread.start()
    bot_thread.start()
    updates_thread.start()