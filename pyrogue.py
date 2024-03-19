import asyncio
import subprocess
import time

import redis


def run_script(script_name):
    return subprocess.Popen(["python", script_name], shell=False)

# timeout in s between bot cycles
TIMEOUT = 100


# proc1.kill()
# proc1.wait()

# proc2.kill()
# proc2.wait()


async def main():
    r = redis.Redis(host='localhost', port=6379, db=0)
    bot1_code = open("bot1.py").read()
    bot2_code = open("bot2.py").read()

    
    proc1 = run_script("bot1.py")
    # proc2 = run_script("bot2.py")

    pubsub = r.pubsub()
    pubsub.subscribe('bot1')
    
    
    round = 0
    for _ in range(10):
        input("---")
        round += 1

        r.publish('cycle', f'{round}')
        await asyncio.sleep(0.5)
        
        message = pubsub.get_message()
        # print("got message", message['data'])
    
    r.publish('cycle', 'STOP')




if __name__ == "__main__":
    asyncio.run(main())