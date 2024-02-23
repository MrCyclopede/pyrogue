import asyncio

# empty, player1, player2, bullet
assets =  ["_", '1', '2', 'x']




class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.map = [[0 for _ in range(width)] for i in range(height)]
    
    def print(self):
        for i in range(self.height):
            for j in range(self.width):
                print(assets[self.map[i][j]], end = " ")
            print()



class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 10


async def main():
    bot1_code = open("bot1.py").read()
    bot2_code = open("bot2.py").read()

    queue = asyncio.Queue()
    
    
    exec(bot1_code, locals())
    exec(bot2_code, locals())
    
    
        
    while True:
        input("---")
        await asyncio.sleep(0)
        await queue.put("SALUT")
        await queue.put("SALUT")




if __name__ == "__main__":
    asyncio.run(main())
        
    