import socket
from _thread import *
import sys
from random import randint
server = "192.168.137.1"
port = 5014

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(s):
    s = s.split(",")
    return int(s[0]), int(s[1]), int(s[2]), int(s[3])


def make_pos(tup):
    print(tup)
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

class Ball:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.vel = 2
        self.cir = ((0,0,255),(cx,cy),5)
        self.m = self.n = 1
    def move(self,x1,x2,y1,y2):
        self.cx += self.vel*self.m
        self.cy += self.vel*self.n
        if self.cx <=0 or self.cx>=500: self.m*=-1
        if self.cy <=0 or self.cy>=500: self.n*=-1
        if (self.cx in range(x1,x1+100) or self.cx in range(x2, x2+100)) and (self.cy == 52 or self.cy==450):
            if (self.cx in range(x1,x1+100)and self.cy in range(y1,y1+3)) or (self.cx in range(x2,x2+100)and self.cy in range(y2,y2+3)): 
                self.n*=-1

currentPlayer = 0
pos = [(200, 450,250,250),(200, 50,250,250)]
b = Ball(250, 250)
        

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if currentPlayer==2:
                pos[(not player)] = pos[(not player)][:2]+(b.cx, b.cy)
                b.move(pos[0][0], pos[1][0], pos[0][1], pos[1][1])
            
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending : ", reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    