import asyncio
import time


async def main():
    while True:
        await queue.get()
        print("bot1 cycle")
        await asyncio.sleep(0)
    


asyncio.get_running_loop().create_task(main())

