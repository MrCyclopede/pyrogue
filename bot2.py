import asyncio


async def main():
    while True:
        await queue.get()
        print("bot2 cycle")
        await asyncio.sleep(0.1)
    


asyncio.get_running_loop().create_task(main())


