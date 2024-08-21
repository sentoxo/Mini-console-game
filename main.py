import os, time
import keyboard

WIDTH = 40
HEIGHT = 40

class Object():
    posX: int
    posY: int
    texture: str
    sizeX: int
    sizeY: int
    speedX: int = 0
    speedY: int = 0
    
    def __init__(self, texture: str, sizeX: int, sizeY: int, posX: int = 1, posY: int = 1) -> None:
        self.texture = texture
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.posX = posX
        self.posY = posY
        
    def setSpeed(self, speedX: int = 0, speedY: int = 0) -> None:
        self.speedX = speedX
        self.speedY = speedY
    
    def move(self, course: str) -> None:
        if course == 'up' and self.posY>1:
            self.posY -= 1
        elif course == 'down' and self.posY<(HEIGHT-1-self.sizeY):
            self.posY += 1
        elif course == 'left' and self.posX>1:
            self.posX -= 1
        elif course == 'right' and self.posX<(WIDTH-1-self.sizeX):
            self.posX += 1
        

def generateBorder(buf: list, x: int, y: int) -> None:
    for i in range(x):
        buf[0][i] = '#'
        buf[y][i] = '#'
    for i in range(y):
        buf[i][0] = '#' #left column
        buf[i][x] = '#' #right column

def addObjectToBuf(buf: list, obj: Object) -> None:
    for i, s in enumerate(obj.texture):
        buf[obj.posY+(i//obj.sizeY)][obj.posX+(i%obj.sizeX)] = s
    
def render(buf: list) -> None:
    os.system("cls")
    s = ''
    for line in buf:
        for char in line:
            s += char + ' '
        s += '\n'
    print(s)    
        
def loop() -> None:
    frameI = 0 
    ball = Object('OOOOOOOOO', 3, 3)
    
    while 1:
        frameI += 1
        buf = [[' ']*WIDTH for i in range(HEIGHT)]
        
        if keyboard.is_pressed("a"):
            ball.move('left')
        elif keyboard.is_pressed("d"):
            ball.move('right')
        elif keyboard.is_pressed("w"):
            ball.move('up')
        elif keyboard.is_pressed("s"):
            ball.move('down')
        generateBorder(buf, WIDTH-1, HEIGHT-1)
        addObjectToBuf(buf, ball)
        render(buf)
        print(str(frameI))
        time.sleep(0.1)
    
    
    
def main():
    loop()
    
if __name__ == "__main__":
    main()