import asyncio
import websockets


async def handshake(websockets):
    fen = await websockets.recv()
    print(fen)
    greatings = f'received {fen}'
    await websockets.send(greatings)
    print("sent to client"+greatings)


async def main():
    async with websockets.serve(handshake, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    print("server started")
    asyncio.run(main())
