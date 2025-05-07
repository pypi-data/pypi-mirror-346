import asyncio
import websockets

async def handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    finally:
        print("Client disconnected")

async def main():
    server = await websockets.serve(handler, "localhost", 9000)
    print("Server started at ws://localhost:9000")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
