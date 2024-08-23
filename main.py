import os, time, sys
import logging, random
import keyboard

WIDTH = 40
HEIGHT = 40
DEBUG = False


class Object():
    counter: int = 0
    id: int
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
        Object.counter +=1
        self.id = Object.counter
        
    def __str__(self) -> str:
        return f'Object {self.id} -> Size X/Y: {self.sizeX}/{self.sizeY}, Pos X/Y: {self.posX}/{self.posY}'
        
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
        buf[0][i] = str(i)[0] if DEBUG else '#'
        buf[y][i] = '#'
    for i in range(y):
        buf[i][0] = str(i)[0] if DEBUG else '#'
        buf[i][x] = '#' #right column

def addObjectToBuf(buf: list, obj: Object) -> None:
    #logging.debug(str(obj))
    for i, s in enumerate(obj.texture):
        try:
            buf[obj.posY+(i//obj.sizeX)][max(obj.posX+(i%obj.sizeX),0)] = s
        except IndexError:
            pass
    
def render(buf: list, f: int) -> None: 
    s = ''
    for line in buf:
        for char in line:
            s += char + ' '
        s += '\n'
    s += str(f)
    os.system("cls")
    sys.stdout.write(s)    
    
def detectCollision(player: Object, objects: list) -> bool:
    for x in objects:
        if isCollision(player, x):
            return True
    return False
       
def isCollision(rect1: Object, rect2: Object) -> bool:
    if rect1.posX >= rect2.posX + rect2.sizeX or rect2.posX >= rect1.posX + rect1.sizeX:
        return False
    if rect1.posY >= rect2.posY + rect2.sizeY or rect2.posY >= rect1.posY + rect1.sizeY:
        return False
    return True
      
        
def loop() -> None:
    frameI = 0 
    ball = Object('/O\OOO\O/', 3, 3, 4, 6)
    objects = [] 
    textLines = '' 
    points = 0
    speed = 40

    while 1:
        frameI += 1
        buf = [[' ']*WIDTH for i in range(HEIGHT)]
        
        if keyboard.is_pressed("space"):
            ball.jump(3)
        elif keyboard.is_pressed("p"): #pause
            keyboard.wait('p')
        elif keyboard.is_pressed("esc"):
            exit()
 
        if frameI % 40 == 0:
            speed -= 1

        ball.updateGravity()
        generateBorder(buf, WIDTH-1, HEIGHT-1)
        addObjectToBuf(buf, ball)
        
        if frameI % speed == 0:
            objects.append(ob := Object('OOOOO'*10, 5, 10, 40, random.randint(1, 29)) )
            logging.debug(str(ob))
        
        for i in range(len(objects)):
            addObjectToBuf(buf, objects[i])
            objects[i].posX -=1 
            
        for i in range(len(objects)):
            if objects[i].posX <= -5:
                del objects[i]
                points += 1
                break
        
        textLines = f"Frames {frameI} \nPoints: {points}\n"
        render(buf, textLines)
        time.sleep(0.05)
        if detectCollision(ball, objects):
            raise exit("Game over motherfucker") 
    
    
def main():
    logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        loop()
    except KeyboardInterrupt:
        pass
    
if __name__ == "__main__":
    main()