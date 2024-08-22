import os, time, sys
import keyboard

WIDTH = 40
HEIGHT = 40

class Object():
    posX: int
    posY: int
    texture: str
    sizeX: int
    sizeY: int
    _speedX: float = 0.0
    _speedY: float = 0.0
    
    def __init__(self, texture: str, sizeX: int, sizeY: int, posX: int = 1, posY: int = 1) -> None:
        self.texture = texture
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.posX = posX
        self.posY = posY
        
    def updateGravity(self) -> None:
        self._speedY += 0.5 #gravity constant
        self.posY += int(self._speedY)
        if self.posY >= HEIGHT-self.sizeY-1:
            self.posY = HEIGHT-self.sizeY-1
            self._speedY = 0.0
        elif self.posY < 1:
            self.posY = 1
            self._speedY = 0.0
    
    def move(self, course: str) -> None:
        if course == 'up' and self.posY>1:
            self.posY -= 1
        elif course == 'down' and self.posY<(HEIGHT-1-self.sizeY):
            self.posY += 1
        elif course == 'left' and self.posX>1:
            self.posX -= 1
        elif course == 'right' and self.posX<(WIDTH-1-self.sizeX):
            self.posX += 1
    
    def jump(self, jumpPower: float) -> None:
        if self._speedY >= 0:
            self._speedY -= jumpPower
        

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
    
def render(buf: list, f: int) -> None: 
    s = ''
    for line in buf:
        for char in line:
            s += char + ' '
        s += '\n'
    s += str(f)
    os.system("cls")
    sys.stdout.write(s)    
    
        
def loop() -> None:
    frameI = 0 
    ball = Object('OOOOOOOOO', 3, 3, 2, 6)

    while 1:
        frameI += 1
        buf = [[' ']*WIDTH for i in range(HEIGHT)]
        
        if keyboard.is_pressed("space"):
            ball.jump(3)
            
        ball.updateGravity()
        generateBorder(buf, WIDTH-1, HEIGHT-1)
        addObjectToBuf(buf, ball)      
        render(buf, frameI)
        time.sleep(0.05)
    
    
def main():
    try:
        loop()
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    main()