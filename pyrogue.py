import asyncio
import subprocess
import time
import signal
import sys

import redis


def run_script(script_name):
    return subprocess.Popen(["python3", script_name], shell=False)

# timeout in s
TIMEOUT = 0.5


# proc1.kill()
# proc1.wait()

# proc2.kill()
# proc2.wait()


async def main():

    r = redis.Redis(host='localhost', port=6379, db=0)
    

    
    proc1 = run_script("bot1.py")
    # proc2 = run_script("bot2.py")

    pubsub = r.pubsub()
    pubsub.subscribe('bot1')
    
    
    def exit_gracefully(signal, frame):
        proc1.kill()
        proc1.wait()
        sys.exit(0)
    signal.signal(signal.SIGINT, exit_gracefully)



    round = 0
    while True:
        input("---")
        # print("===")
        round += 1

        r.publish('cycle', f'{round}')
        
        
        message = None
        round_start = time.time()
        print( time.time() - round_start)
        while (message == None or message['type'] != 'message'):
            
                # break

            message = pubsub.get_message()
            if time.time() - round_start > TIMEOUT:
                print("TIMEOUT")
            time.sleep(0.1)

        print("bot1:", message)
    
    
    exit_gracefully()




if __name__ == "__main__":
    asyncio.run(main())