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

r = redis.Redis(host='localhost', port=6379, db=0)

def all_processes_done(processes):
    for k,v in processes.items():
        if not v['done']:
            return False
    else:
        return True


def run_game(players):
    processes = {}
    pubsub = r.pubsub()

    for player_name in players:
        p = run_script(f"{player_name}.py")
        processes[player_name] = {'done': False, 'p_handle': p}
        pubsub.subscribe(f'{player_name}')

    print(processes)

    
    def kill_all_bots():
        for p_name,p in processes.items():
            
            p['p_handle'].kill()
            p['p_handle'].wait()
            print(f"killed {p_name}")
        sys.exit(0)
        

    def signal_handler(signal, frame):
        kill_all_bots()
        

    signal.signal(signal.SIGINT, signal_handler)


    #let time for processes to start and connect to redis
    time.sleep(0.1)
    round = 0
    while True:
        # input("---")
        print("===")
        round += 1

        for i,_ in enumerate(processes):
            r.publish(f'cycle{i + 1}', f'{round}')
        
        
        message = None
        cycle_start = time.time()

        while not all_processes_done(processes):
            
            while (message == None or message['type'] != 'message'):
                if time.time() - cycle_start > TIMEOUT:
                    for p in processes:
                        if not p: 
                            print("bot1", end="")
                    print("TIMEOUT")
                    kill_all_bots()

                message = pubsub.get_message()
            else:
                processes[message['channel'].decode()]['done'] = True
                print(message['channel'].decode(), message['data'].decode())
                message = None

        for p,v in processes.items():
            v['done'] = False

    kill_all_bots()
    

def main():
    run_game(["bot1", "bot2"])
   

if __name__ == "__main__":
    main()