import pygame, sys, time

class ball:
    def __init__( self, screen, color, posX, posY, radius ):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def startMoving(self):
        self.dx = 9
        self.dy = 3

    def move(self):
	    self.posX += self.dx
	    self.posY += self.dy

    def paddleCollision(self):
        self.dx = -self.dx

    def wallCollision(self):
        self.dy = -self.dy

    def restartPosition(self):
        self.posX = Width//2
        self.posY = Height//2
        self.dx = 0
        self.dy = 0
        self.show()

class paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = "stopped"
        self.show()

    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width,self.height))

    def move(self):
        if self.state == "up":
            self.posY -= 15
        elif self.state == "down":
            self.posY += 15

    def clamp(self):
        if self.posY <= 0:
            self.posY = 0

        if self.posY + self.height >= Height:
            self.posY = Height - self.height

    def restartPosition(self):
        self.posY = Height//2 - self.height//2
        self.state = "stopped"
        self.show()


class collisionManager:
    def ballPaddleLeft(self,ball, paddleLeft):
        if ball.posY + ball.radius > paddleLeft.posY and ball.posY - ball.radius < paddleLeft.posY + paddleLeft.height:
            if ball.posX - ball.radius <= paddleLeft.posX + paddleLeft.width:
                return True
        return False

    def ballPaddleRight(self,ball, paddleRight):
        if ball.posY + ball.radius > paddleRight.posY and ball.posY - ball.radius < paddleRight.posY + paddleRight.height:
            if ball.posX + ball.radius >= paddleRight.posX :
                return True
        return False

    def ballWall(self,ball):
        if ball.posY - ball.radius <= 0:
            return True
        
        if ball.posY + ball.radius >= Height:
            return True
        
        return False

    def checkGoalLeft(self, ball):
        return balls.posX - balls.radius >= Width

    def checkGoalRight(self, ball):
        return balls.posX + balls.radius <= 0


class score:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont('monospace', 80, bold= True)
        self.label = self.font.render(self.points,0,neon)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX-self.label.get_rect().width//2,self.posY))

    def increaseScore(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points,0,neon)

    def scoreRestart(self):
        self.points = "0"
        self.label = self.font.render(self.points,0,neon)



pygame.init()

Width = 1080
Height = 720
FPS = 60

black = (0,0,0)
white = (255,255,255)
neon = (57,255,20)

screen = pygame.display.set_mode( (Width,Height) )
pygame.display.set_caption("King Pong")
clock = pygame.time.Clock()

def paintBG():
    screen.fill( black )
    pygame.draw.line(screen, white, (Width//2, 0),(Width//2, Height),5)


def restart():
    paintBG()
    scoreLeft.scoreRestart()
    scoreRight.scoreRestart()
    balls.restartPosition()
    paddleLeft.restartPosition()
    paddleRight.restartPosition()

paintBG()


balls = ball( screen, neon, Width//2, Height//2, 15)
paddleLeft = paddle(screen, white , 15, Height//2-60,20,120)
paddleRight = paddle(screen, white , Width-20-15, Height//2-60,20,120)
collision = collisionManager()
scoreLeft = score(screen,"0",Width//4,15)
scoreRight = score(screen,"0",Width - Width//4,15)

font = pygame.font.SysFont('arial', 20)
credit = font.render('@made by SURYA in association with google.com', True, neon)
fontx = pygame.font.SysFont('arial', 45)
message = fontx.render('Thank You for playing King Pong!!', True, neon)
fontz = pygame.font.SysFont('times new roman', 20)
leftIns = fontz.render("Press ' w ' and ' s ' to Move the Paddle!", True, neon)
RightIns = fontz.render("Press UP and DOWN Key to Move the Paddle!", True, neon)
start = fontz.render("Press ' n ' to Start the Game!", True, neon)
newGame = fontz.render("Press ' r ' to Restart the Game!", True, neon)

playing = False

while True:
    screen.blit(start, [155,660])
    screen.blit(newGame, [690,660])
    screen.blit(leftIns, [110,690])
    screen.blit(RightIns, [620,690])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.fill(black)
            screen.blit(message, [Width//2-272.5,Height//2-100])
            screen.blit(credit, [Width//2-175,685])
            pygame.display.update()
            time.sleep(3)
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                balls.startMoving()
                playing = True
            
            if event.key == pygame.K_r:
                restart()
                playing = False

            if event.key == pygame.K_w:
                paddleLeft.state = "up"
            
            if event.key == pygame.K_s:
                paddleLeft.state = "down"

            if event.key == pygame.K_UP:
                paddleRight.state = "up"

            if event.key == pygame.K_DOWN:
                paddleRight.state = "down"
        if event.type == pygame.KEYUP:
            paddleLeft.state = "stopped"
            paddleRight.state = "stopped"
    
    if playing:
        paintBG()

        balls.move()
        balls.show()

        paddleLeft.move()
        paddleLeft.clamp()
        paddleLeft.show()

        paddleRight.move()
        paddleRight.clamp()
        paddleRight.show()

        if collision.ballPaddleLeft(balls,paddleLeft):
            balls.paddleCollision()
        
        if collision.ballPaddleRight(balls,paddleRight):
            balls.paddleCollision()

        if collision.ballWall(balls):
            balls.wallCollision()

        if collision.checkGoalLeft(ball):
            paintBG()
            scoreLeft.increaseScore()
            balls.restartPosition()
            paddleLeft.restartPosition()
            paddleRight.restartPosition()
            playing = False

        if collision.checkGoalRight(ball):
            paintBG()
            scoreRight.increaseScore()
            balls.restartPosition()
            paddleLeft.restartPosition()
            paddleRight.restartPosition()
            playing = False

    

    scoreLeft.show()
    scoreRight.show()

    clock.tick(FPS)
    pygame.display.update()