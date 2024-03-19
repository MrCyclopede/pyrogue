import asyncio

import redis


async def subscribe_to_channel():
    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('cycle')
    while True:
        message = pubsub.get_message()
        if message:
            print(f"Subscriber 2 received message: {message['data']}")

# Example usage
asyncio.run(subscribe_to_channel())
