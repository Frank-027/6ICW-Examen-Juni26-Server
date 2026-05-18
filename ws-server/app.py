from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random

app = FastAPI()

students = {
    "A7K9Q2": "Mats",
    "B3X8Z1": "Dylan",
    "C9D2P5": "Maarten",
    "Z1Q8M7": "Noah",
    "L4T6V9": "Kevin",
    "F5W3R2": "Max-Emile"
}

with open("levenswijsheden.txt", "r", encoding="utf-8") as f:
        spreuken = f.readlines()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # 1. auth ontvangen
        api_key = await ws.receive_text()
        print(f"Received API key: {api_key}")

        if api_key not in students:
            await ws.send_text("ERROR: INVALID API KEY")
            await ws.close()
            return

        naam = students[api_key]
        print(f"Authenticated user: {naam}")

        # 2. init response (optioneel maar handig)
        await ws.send_text(f"CONNECTED: {naam}")
        print(f"{naam} connected with API key {api_key}")

        # 3. continue loop voor "get" requests
        while True:
            print(f"Waiting for message from {naam}...")
            msg = await ws.receive_text()

            if msg == "get":
                boodschap = random.choice(spreuken).strip()
                print(f"Sending to {naam}: {boodschap}")

                await ws.send_text(boodschap)
            else:
                print(f"Unknown command from {naam}: {msg}")
                await ws.send_text("ERROR: UNKNOWN COMMAND")

    except WebSocketDisconnect:
        print(f"{naam} disconnected")
    except Exception as e:
        print("Error:", e)