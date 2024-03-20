import time

import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def wait(cycles):
    
    
    while cycles > 0:
        message = None
        while message == None or message['type'] != 'message':
            message = pubsub.get_message()
            time.sleep(0.1)
        if cycles > 1:
            r.publish('bot1', f"wait")
        cycles -= 1

            
            
pubsub = r.pubsub()
pubsub.subscribe('cycle')


def move():
    wait(2)
    r.publish('bot1', 'move')

def shoot():
    wait(1)
    r.publish('bot1', 'shoot')

def rotate():
    wait(1)
    r.publish('bot1', 'rotate')



while True:
    move()
    shoot()
    time.sleep(2)
    rotate()
