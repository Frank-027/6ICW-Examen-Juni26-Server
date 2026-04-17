from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
import json

app = FastAPI()
bericht = ( 
    "Veel succes met de examens, geniet daarna van een welverdiend verlof "
    "en vooral: geloof in jezelf en maak iets moois van alles wat nog komt"
    " – in je studies, je werk en je leven."

    "Het was fijn om jullie de voorbije twee jaar iets te mogen bijbrengen "
    "en jullie te zien groeien – ik wens jullie het allerbeste!" 
    "                                                                      "
    "                                                       Frank Demonie"
)

students = {
    "A7K9Q2": ("Mats", random.randint(1, 26)),
    "B3X8Z1": ("Dylan", random.randint(1, 26)),
    "C9D2P5": ("Maarten", random.randint(1, 26)),
    "Z1Q8M7": ("Noah", random.randint(1, 26)),
    "L4T6V9": ("Kevin", random.randint(1, 26)),
    "F5W3R2": ("Max-Emile", random.randint(1, 26))
}

def caesar_encrypt(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char

    return result

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # 1. auth ontvangen
        api_key = await ws.receive_text()

        if api_key not in students:
            await ws.send_text("ERROR: INVALID API KEY")
            await ws.close()
            return

        naam, caesarcode = students[api_key]

        # 2. init response (optioneel maar handig)
        await ws.send_text(f"CONNECTED: {naam}")
        print(f"{naam} connected with API key {api_key} and Caesar code {caesarcode}")

        # 3. continue loop voor "get" requests
        while True:
            msg = await ws.receive_text()

            if msg == "get":
                encrypted_name = caesar_encrypt(naam, caesarcode)
                encrypted_boodschap = caesar_encrypt(bericht, caesarcode)

                data = {
                    "encrypted_name": encrypted_name,
                    "caesarcode": caesarcode,
                    "encrypted_boodschap": encrypted_boodschap
                }
                json_message = json.dumps(data)
                await ws.send_text(json_message)
            else:
                await ws.send_text("ERROR: UNKNOWN COMMAND")

    except WebSocketDisconnect:
        print(f"{naam} disconnected")
    except Exception as e:
        print("Error:", e)