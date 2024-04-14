import asyncio
import websockets


async def handshake():
    url = "ws://localhost:8765"
    async with websockets.connect(url) as websocket:
        fen = input("give me a fen ")
        await websocket.send(fen)
        print("client send"+fen)
        greatings = await websocket.recv()
        print("recived from server"+greatings)

if __name__ == "__main__":
    print("client started")
    asyncio.run(handshake())
