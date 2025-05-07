import asyncio
import websockets
import json
import os

uri = "ws://localhost:9000/ws" 

async def websocket_client():
    while True: 
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to the WebSocket server.")

                while True:
                    if os.path.exists("player_state.json"):
                        with open("player_state.json", "r") as file:
                            player_state = json.load(file)
                            print(f"Sending player state: {player_state}")

                        # Send user state as JSON
                        await websocket.send(json.dumps(player_state))
                        print(f"Sent: {player_state}")

                    # Receive response from server
                    response = await websocket.recv()
                    print(f"Received from server: {response}")

                    # Wait for 5 seconds before sending the next update
                    await asyncio.sleep(5)

        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.WebSocketException) as e:
            print(f"Connection lost. Reconnecting in 5 seconds... Error: {e}")
            await asyncio.sleep(5)  # Wait 5 seconds before trying to reconnect

# Run the WebSocket client
if __name__ == "__main__":
    asyncio.run(websocket_client())