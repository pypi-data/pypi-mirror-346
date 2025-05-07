from .main import GameEngine
import asyncio

def main():
    """Entry point for the application.
    
    Creates and runs the game engine with specified server and frame rate.
    """
    FPS = 60
    SERVER = "ws://localhost:8000/ws"
    gm = GameEngine(SERVER, FPS)
    asyncio.run(gm.run())

if __name__ == "__main__":
    main()
