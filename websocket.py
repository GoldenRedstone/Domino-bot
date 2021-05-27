import http.server
import socketserver
import os
import json
import math

import pygame
pygame.init()

if os.path.dirname(__file__) != "":
    os.chdir(os.path.dirname(__file__))


# math.dist dont work
def distance(a, b):
    xd = a[0] - b[0]
    yd = a[1] - b[1]
    return (xd**2 + yd**2)**0.5


# Reduces the size of the list of points used
# divides the length by the number specified
def cull(list, number=2):
    newList = []
    for n in range(len(list)):
        if n % number == 0:
            newList.append(list[n])
    return newList


# Reduces unneccisary points from the list
# while keeping points neccisary to stay within angle
def simplify(list, max_distance_off_line=10, dist_back=2):
    newList = []

    # Start with a as first point
    an = 0
    bn = 1
    a = list[an]
    b = list[bn]

    newList.append(a)

    for cn in range(2, len(list)-2):
        try:
            c = list[cn]
            # creates linear function using points a and b
            fm = (b[1]-a[1])/(b[0]-a[0])
            fc = b[0]*fm - b[1]
            # calculate c distance from line
            dist_off_line = abs(-fm*c[0] + c[1] + fc) / (fm**2 + 1)**0.5
            if dist_off_line > max_distance_off_line:
                newList.append(list[round(cn-2)]) # Using <cn-2 is risky but better
                an = bn
                bn = cn - dist_back
                a = list[an]
                b = list[bn]
            else:
                pass
        except ZeroDivisionError:
            # Update line without extending the list
            an = bn
            bn = cn - 3
            a = list[an]
            b = list[bn]

    newList.append(list[-1])
    return newList

# Draws a list to the screen
# Does not update pygame afterwards


def draw(list, k=1, clear=True, colour=(255, 255, 255)):
    global screen
    if clear:
        screen = pygame.display.set_mode((500, 500))
        screen.fill((0, 0, 0))
        # for i in list:
        #     pygame.draw.circle(screen, (255, 255, 255),
        #                        (round(i[0]), round(i[1])), 10)
    pygame.draw.lines(screen, colour, False, list, 5)


# Determines the angle between three points
def find_angle(a, b, c):
    ba = (a[0]-b[0], a[1]-b[1])
    bc = (c[0]-b[0], c[1]-b[1])

    dot = ba[0]*bc[0] + ba[1]*bc[1]

    magBA = (ba[0]**2 + ba[1]**2)**0.5
    magBC = (bc[0]**2 + bc[1]**2)**0.5

    try:
        angle = math.acos(round(dot/(magBA*magBC), 5))
        angle = math.degrees(angle)
    except ZeroDivisionError:
        angle = 180

    return angle, ba, bc

    '''
    try:
        angle = math.acos(round(dot/(magBA*magBC), 5))
        angle = math.degrees(angle)
        return angle
    except ZeroDivisionError:
        print(a,b,c)
        # raise "ZeroDivisionError"
        return None
    '''


# Currently prints, and decides whether the angle is appropriate
# MinAngle and MaxAngle create an acceptable range:  min < θ < max
def reduce_angle(list, minAngle, adjust=0.5):
    newList = []
    newList.append(list[0])
    good = 0
    bad = 0
    for i in range(len(list)-2):
        a = list[i]
        b = list[i+1]
        c = list[i+2]

        angle, ba, bc = find_angle(a, b, c)
        # print(round(angle))

        newb = [0, 0]

        if angle < minAngle:  # If points are too close, skip them. resolved later
            # print("GOOD")
            newb[0] = b[0]
            newb[1] = b[1]
            good += 1
        else:
            # print(i, end=" ")
            # b = tuple(b[n] + ba[n]*adjust + bc[n]*adjust for n in range(2))
            newb[0] = b[0] + ba[0]*adjust + bc[0]*adjust
            newb[1] = b[1] + ba[1]*adjust + bc[1]*adjust
            bad += 1

        newList.append(newb)

    newList.append(list[-1])

    print(bad, "points reduced", round(bad/len(list), 2)*100)

    return newList


class Server(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = body.decode("UTF-8")
        data = json.loads(data)
        points = data["points"]
        print("")
        print("Button Pressed!")

        if len(points) > 20:

            # Received points
            print(len(points), "points received")
            draw(points, clear=True, colour=(95, 85, 85))

            # Reduced points
            # while True:
            #     newPoints = reduce_angle(points, 100)
            #     if newPoints == points:
            #         break
            #     else:
            #         points = newPoints
            #         draw(points, clear=False, colour=(70, 70, 80))
            #         pygame.display.update()

            # draw(points, clear=False, colour=(170, 170, 180))

            # Culled points
            points = simplify(points, 10)
            print(len(points), "points rendered")
            draw(points, clear=False)

            pygame.display.update()
        else:
            print("Drawing too small!")


def runWebsite(ip):
    print("Started")
    print("")
    socketserver.TCPServer((ip, 8000), Server).serve_forever()


if __name__ == "__main__":
    runWebsite("127.0.0.1")
