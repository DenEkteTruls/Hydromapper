from bdb import effective
import socket
import pygame

class Networking:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    def send(self, msg):

        self.server.sendto(msg.encode(), (self.host, self.port))

    
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((500, 500))

speed = 0
heading = 0

net = Networking("192.168.4.1", 8081)

def renderText(text, pos, renderer):
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render(text, False, (255, 255, 255))
    renderer.blit(textsurface,(pos[0], pos[1]))


# start AP : m
# stop AP : n
# stop everything : j
# return home : h

print("Arm\t\t:\to\nDisarm\t\t:\tl\nReturn Home\t:\th\nStart AP\t:\tk\nStop AP\t\t:\tm\nKILL\t\t:\ty\n")

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                speed += 1
                net.send("0x1"+str(speed))
            elif event.key == pygame.K_s:
                speed -= 1
                net.send("0x1"+str(speed))
            elif event.key == pygame.K_a:
                heading += 3
                if heading < 60 and heading > -60:
                    if heading > 0:
                        net.send("2x+"+str(heading))
                    else:
                        net.send("2x"+str(heading))
            elif event.key == pygame.K_d:
                heading -= 3
                if heading < 60 and heading > -60:
                    if heading > 0:
                        net.send("2x+"+str(heading))
                    else:
                        net.send("2x"+str(heading))
            elif event.key == pygame.K_o:
                net.send("0x0001") # arm
            elif event.key == pygame.K_l:
                net.send("0x0010") # disarm
            elif event.key == pygame.K_SPACE:
                heading = 0        # heading
                net.send("2x+"+str(heading))

            elif event.key == pygame.K_h:
                net.send("1x0000") # return to home
            elif event.key == pygame.K_k:
                net.send("1x0001") # start AP
            elif event.key == pygame.K_m:
                net.send("1x0011") # stop AP
            elif event.key == pygame.K_y:
                net.send("3x0000") # Total kill


    screen.fill((0, 0, 0))
    
    renderText(f"Speed: {speed}%", (100, 150), screen)
    renderText(f"Heading: {heading}*", (100, 250), screen)

    pygame.display.flip()

pygame.quit()
exit(0)
