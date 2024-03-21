import subprocess
import time
import signal
import sys

from abc import ABC, abstractmethod
import redis

class GameState:
    def __init__(self, player_list):
        self.arena = Arena()
        self.players = []

        for player in player_list:
            bot = PlayerBot(player, 0 + len(self.players * 2), 0, 1, 10)
            self.players.append(bot)
            self.arena.summon_player(bot)

        self.arena.print()


# Move 
# Scan -/ 
# Summon
# tick 
# wait

# class Spell(ABC):
#     @abstractmethod
#     def cast(self):
#         pass

# class MoveSpell(Spell, ABC):
#     pass

# class simple_move(MoveSpell):
#     pass

# class strafe(MoveSpell):
#     pass


def simple_move(self, summonable, arena):
    direction = self.summonable.direction
    if direction == 1 and self.summonable.y > 0:
        self.summonable.y -= 1
    elif direction == 2 and self.summonable.x < self.arena.width - 1:
        self.summonable.x += 1
    elif direction == 3 and self.summonable.y < self.arena.height - 1:
        self.summonable.y += 1
    elif direction == 4 and self.summonable.x > 0:
        self.summonable.x -= 1
    
class SummonSpell(Spell, ABC):
    def __init__(self, summonable):
        self.summonable = summonable



class ScanSpell(Spell, ABC):
    pass



class Summonable(ABC):
    def __init__(self, name, x, y, max_hp, arena):
        self.name = name
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.hp = max_hp
        self.arena = arena
  

    def __repr__(self):
        return f"{self.name[:1]}"
    
    #maybe move logic should be here
        
    @abstractmethod
    def tick(self):
        pass
    
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def scan(self):
        pass
    
    @abstractmethod
    def summon(self):
        pass

    def wait(self):
        pass

class PlayerBot(Summonable):
    def __init__(self, name, x, y, direction, max_hp):
        super().__init__(name, x, y, max_hp)
        self.direction = direction

    def tick(self):
        print("tick")


class Arena:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.map = [["_" for _ in range(width)] for _ in range(height)]
        self.summoned_objects = []

    def tick(self):
        for obj in self.summoned_objects:
            obj.tick()

    def print(self):
        for row in self.map:
            for cell in row:
                print(cell, end="")
            print()


    def summon_player(self, obj):
        if isinstance(obj, Summonable):
            self.summoned_objects.append(obj)
            self.map[obj.y][obj.x] = obj
        else:
            raise TypeError("Object must be of type Summonable")

    

game = GameState(["bot1", "bot2"])


# print(a)
sys.exit()




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
                    for pname,p in processes.items():
                        if not p['done']: 
                            print(pname, end="")
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


if __name__ == "__main__":
    run_game(["bot1", "bot2"])