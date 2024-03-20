import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def wait(cycles):
    
    
    while cycles > 0:
        message = None
        while message == None or message['type'] != 'message':
            message = pubsub.get_message()
        if cycles > 1:
            r.publish('bot2', f"wait")
        cycles -= 1

            
            
pubsub = r.pubsub()
pubsub.subscribe('cycle2')


def move():
    wait(2)
    r.publish('bot2', 'move')

def shoot():
    wait(1)
    r.publish('bot2', 'shoot')

def rotate():
    wait(1)
    r.publish('bot2', 'rotate')



while True:
    move()
    shoot()
    rotate()
