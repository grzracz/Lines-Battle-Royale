from queue import *
import pygame
import socket
import threading
import time
import random
import sys


class Server:
    def __init__(self, host_addr, port):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()
        self.host = host_addr
        self.port = port
        self.client = ""
        self.connected = ""
        self.q = Queue(5)
        self.color = (255, 255, 255)

    def clear_queue(self):
        while not self.q.empty():
            self.q.get()

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        print("Server running:", self.host + ":" + str(self.port))
        serversocket.listen(1)
        while True:
            (clientsocket, address) = serversocket.accept()
            self.client = clientsocket.recv(64).decode()
            print("Client with address", self.client, "connected to socket", self.host + ":" + str(self.port))
            self.connected = True
            # CAN DO SOMETHING HERE WITH THE CLIENT YOU ARE CONNECTED TO
            while True:
                info = clientsocket.recv(128)
                if not info:
                    break
                # DO SOMETHING WITH WHAT WAS SENT
                command = info.decode()
                if command == "LEFT" or command == "RIGHT" or command == "UP" or command == "DOWN":
                    if self.q.full():
                        print(self.client + ":", "queue is full, unable to store command:", command)
                    else:
                        print(self.client + ":", command)
                        self.q.put(command)
                else:
                    print(self.client, "sent an unknown command:", info)

            # DO SOMETHING WHEN CLIENT DISCONNECTS
            self.connected = False
            self.clear_queue()
            print("Client with address", self.client, "disconnected from socket", self.host + ":" + str(self.port))


class Player:
    def __init__(self, server, starting_point, color, direction, speed):
        self.server = server
        self.start_x = starting_point[0]
        self.start_y = starting_point[1]
        self.x = self.start_x
        self.y = self.start_y
        self.color = color
        self.start_direction = direction
        self.direction = self.start_direction
        self.speed = speed
        self.stopped = False
        self.show = True
        self.points = 0

    def change_starting_point(self, point, direction):
        self.start_x = point[0]
        self.start_y = point[1]
        self.x = self.start_x
        self.y = self.start_y
        self.start_direction = direction
        self.direction = self.start_direction

    def stop(self):
        self.stopped = True

    def toggle_show(self):
        temp = random.randint(0, 4)
        if temp == 0:
            self.show = False
        else:
            self.show = True

    def reset(self):
        self.stopped = False
        self.x = self.start_x
        self.y = self.start_y
        self.direction = self.start_direction
        self.show = True

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, box_width, box_width))

    def update(self):
        if not self.stopped:
            self.points += 0.1
            new_direction = self.direction
            if not self.server.q.empty():
                new_direction = self.server.q.get()

            if self.direction == "UP":
                if new_direction != "DOWN":
                    self.direction = new_direction
            elif self.direction == "DOWN":
                if new_direction != "UP":
                    self.direction = new_direction
            elif self.direction == "RIGHT":
                if new_direction != "LEFT":
                    self.direction = new_direction
            elif self.direction == "LEFT":
                if new_direction != "RIGHT":
                    self.direction = new_direction

            if not self.show:
                pygame.draw.rect(screen, C.black, pygame.Rect(self.x, self.y, box_width, box_width))

            check_pixel_1 = (1, 1)
            check_pixel_2 = (1, 1)

            if self.direction == "UP":
                self.y -= self.speed
                if self.y < 1:
                    if self.show:
                        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, box_width, box_width))
                    self.y = height - 1
                check_pixel_1 = (self.x, self.y - 1)
                check_pixel_2 = (self.x + box_width, self.y - 1)
            elif self.direction == "DOWN":
                self.y += self.speed
                if self.y + box_width + 1 > height:
                    if self.show:
                        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, box_width, box_width))
                    self.y = 2 - box_width
                check_pixel_1 = (self.x, self.y + box_width + 1)
                check_pixel_2 = (self.x + box_width, self.y + box_width + 1)
            elif self.direction == "RIGHT":
                self.x += self.speed
                if self.x + box_width + 1 > width:
                    if self.show:
                        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, box_width, box_width))
                    self.x = 2 - box_width
                check_pixel_1 = (self.x + box_width + 1, self.y)
                check_pixel_2 = (self.x + box_width + 1, self.y + box_width)
            elif self.direction == "LEFT":
                self.x -= self.speed
                if self.x < 1:
                    if self.show:
                        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, box_width, box_width))
                    self.x = width - 1
                check_pixel_1 = (self.x - 1, self.y)
                check_pixel_2 = (self.x - 1, self.y + box_width)

            if check_pixel_1[0] < 0:
                check_pixel_1 = (0, check_pixel_1[1])
            if check_pixel_1[0] >= width:
                check_pixel_1 = (width - 1, check_pixel_1[1])
            if check_pixel_1[1] < 0:
                check_pixel_1 = (check_pixel_1[0], 0)
            if check_pixel_1[1] >= height:
                check_pixel_1 = (check_pixel_1[0], height - 1)
            if check_pixel_2[0] < 0:
                check_pixel_2 = (0, check_pixel_2[1])
            if check_pixel_2[0] >= width:
                check_pixel_2 = (width - 1, check_pixel_2[1])
            if check_pixel_2[1] < 0:
                check_pixel_2 = (check_pixel_2[0], 0)
            if check_pixel_2[1] >= height:
                check_pixel_2 = (check_pixel_2[0], height - 1)

            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, box_width, box_width))
            pixel = pygame.Surface.get_at(screen, check_pixel_1)
            pixel2 = pygame.Surface.get_at(screen, check_pixel_2)
            if not (pixel == (0, 0, 0, 255) or pixel == (20, 20, 20, 255)) \
                    or not (pixel2 == (20, 20, 20) or pixel2 == (0, 0, 0, 255)):
                return False
            return True
        else:
            return False


class StartingPoints:
    def __init__(self):
        self.points = []
        for x in range(1, 9):
            for y in range(1, 4):
                temp = 0
                if x % 2 == 0:
                    if y % 2 == 1:
                        self.points.append((int(x * width/10), int(y * height/4), False))
                        temp += 1
                    if y % 2 == 0:
                        self.points.append((int(x * width/10), int(y * height/4), False))
                        temp += 1

    def reset(self):
        for x in range(0, len(self.points) - 1):
            self.points[x] = (self.points[x][0], self.points[x][1], False)

    def random_point(self):
        temp = random.randint(0, len(self.points) - 1)
        while self.points[temp][2]:
            temp = (temp + 1) % len(self.points)
        self.points[temp] = (self.points[temp][0], self.points[temp][1], True)
        return self.points[temp][0], self.points[temp][1]


class Colors:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (20, 20, 20)
        self.deadly_grey = (21, 21, 21)
        self.colors = []
        self.colors.append((255, 0, 0, False))
        self.colors.append((34, 139, 34, False))
        self.colors.append((0, 0, 255, False))
        self.colors.append((255, 255, 0, False))
        self.colors.append((0, 255, 255, False))
        self.colors.append((255, 0, 255, False))
        self.colors.append((255, 102, 178, False))
        self.colors.append((153, 0, 0, False))

    def reset(self):
        for x in range(0, len(self.colors) - 1):
            self.colors[x] = (self.colors[x][0], self.colors[x][1], self.colors[x][2], False)

    def random_color(self):
        temp = random.randint(0, len(self.colors) - 1)
        while self.colors[temp][3]:
            temp = (temp + 1) % len(self.colors)
        self.colors[temp] = (self.colors[temp][0], self.colors[temp][1], self.colors[temp][2], True)
        return self.colors[temp][0], self.colors[temp][1], self.colors[temp][2]


def random_direction():
    temp = random.randint(0, 3)
    if temp == 0:
        return "UP"
    elif temp == 1:
        return "RIGHT"
    elif temp == 2:
        return "DOWN"
    else:
        return "LEFT"


def servers_connected(servers_list):
    for x in range(0, number_of_players):
        if not servers_list[x].connected:
            return False
    return True


def players_connected(players_list):
    for x in range(0, number_of_players):
        if not players_list[x].server.connected:
            return False
    return True


def players_stopped(players_list):
    players_stopped_number = 0
    for x in range(0, number_of_players):
        if players_list[x].stopped:
            players_stopped_number += 1
    if players_stopped_number >= number_of_players - 1:
        return True
    else:
        return False


def find_moving_player(players_list):
    for x in range(0, number_of_players):
        if not players_list[x].stopped:
            return players_list[x]


def get_points(player_input):
    return player_input.points


def draw_menu(players_list, frame_count):
    pygame.draw.rect(screen, C.black, pygame.Rect(width + box_width, 0, width + menu_width, height))
    pygame.draw.rect(screen, C.grey, pygame.Rect(width, 0, box_width, height))
    logo_width = logorect.width
    indent = int((menu_width + box_width - logo_width) / 2)
    logorect.x = width + indent
    logorect.y = int(indent / 2)
    screen.blit(logo, logorect)
    temp_y = logorect.y + logorect.height + int(indent / 2)
    temp_x = width + int(indent / 2)
    screen.blit(text_fieldclosing, (temp_x, temp_y))
    temp_x += int(indent/4)
    temp_y += int(indent/4)
    time_color = C.white
    if waiting_for_round:
        time_left = "10:00"
    elif not fog_closing:
        time_left_seconds = str(9 - int(frame_count / 60))
        time_left_smaller = str(int((60 - frame_count % 60) * 1.6))
        if int(time_left_smaller) < 10:
            time_left_smaller = "0" + str(int(time_left_smaller))
        if frame_count % 60 == 0:
            time_left_seconds = str(int(time_left_seconds) + 1)
            time_left_smaller = "00"
        time_left = str(time_left_seconds + ":" + time_left_smaller)
        if int(time_left_seconds) < 3:
            time_color = (255, 0, 0)
        else:
            time_color = C.white
    else:
        time_color = (255, 0, 0)
        time_left = "Closing..."

    text_timeleft = bigfont.render(time_left, True, time_color)
    rect_width = menu_width - int(1.5 * indent)
    rect_height = 100
    screen.blit(text_timeleft, (temp_x + int((rect_width - text_timeleft.get_width())/2),
                temp_y + int((rect_height - text_timeleft.get_height())/2)))
    temp_x -= int(indent/4)
    temp_y += 2 * int(indent)
    screen.blit(text_ranking, (temp_x, temp_y))
    sorted_players = []
    for x in range(0, number_of_players):
        sorted_players.append(players_list[x])
    sorted_players.sort(key=get_points, reverse=True)
    player_num = 0
    for x in sorted_players:
        temp_y += int(indent/2.5)
        player_num += 1
        text_player_ranking = font.render(str(player_num) + ". Player " + str(x.server.port - (port - 1)) + ": " +
                                          str(int(x.points)) + " points", True, x.color)
        screen.blit(text_player_ranking, (temp_x, temp_y))
    if waiting_for_round:
        temp_x += int(indent / 4)
        temp_y += int(indent * 4)
        text_waiting_for_round = font.render("Next round in:", True, C.white)
        screen.blit(text_waiting_for_round, (temp_x, temp_y))
        temp_y += int(indent / 2)
        text_seconds_to_round = bigfont.render(str(3 - int(frame_count / 60)), True, C.white)
        screen.blit(text_seconds_to_round, (temp_x + int((rect_width - text_seconds_to_round.get_width())/2),
                    temp_y + int((rect_height - text_seconds_to_round.get_height())/2)))
    return sorted_players[0].points


def scale_fog_value(number, value):
    for iter1 in range(0, number):
        value = int(0.75 * value)
    return value


def draw_outline(number):
    outline_width = 5
    current_width = scale_fog_value(number, width)
    current_height = scale_fog_value(number, height)
    indent_x = int((width - current_width) / 2)
    indent_y = int((height - current_height) / 2)
    pygame.draw.rect(screen, C.grey, pygame.Rect(indent_x, indent_y, current_width, outline_width))
    pygame.draw.rect(screen, C.grey, pygame.Rect(indent_x, indent_y, outline_width, current_height))
    pygame.draw.rect(screen, C.grey, pygame.Rect(current_width + indent_x, indent_y, outline_width,
                                                 current_height + outline_width))
    pygame.draw.rect(screen, C.grey, pygame.Rect(indent_x, indent_y + current_height, current_width, outline_width))


def draw_fog(percent, number):
    outline_width = 5
    current_width = scale_fog_value(number, width)
    current_height = scale_fog_value(number, height)
    previous_width = scale_fog_value(number - 1, width)
    previous_height = scale_fog_value(number - 1, height)

    previous_x = int((width - previous_width) / 2)
    previous_y = int((height - previous_height) / 2)
    indent_x = int((previous_width - current_width) * percent/200) + outline_width
    indent_y = int((previous_height - current_height) * percent/200) + outline_width

    pygame.draw.rect(screen, C.deadly_grey, pygame.Rect(0, 0, width, previous_y + indent_y))
    pygame.draw.rect(screen, C.deadly_grey, pygame.Rect(0, 0, previous_x + indent_x, height))
    pygame.draw.rect(screen, C.deadly_grey,
                     pygame.Rect(width - previous_x - indent_x, 0, previous_x + indent_x, height))
    pygame.draw.rect(screen, C.deadly_grey,
                     pygame.Rect(0, height - previous_y - indent_y, width, previous_y + indent_y))


def get_next_color(colors, number):
    while True:
        next_number = (number + 1) % len(colors)
        number = (number + 1) % len(colors)
        if not colors[next_number][3]:
            return next_number


def get_previous_color(colors, number):
    while True:
        next_number = (number - 1) % len(colors)
        number = (number - 1) % len(colors)
        if not colors[next_number][3]:
            return next_number


# GLOBAL VARIABLES/CONSTANTS:
host = "192.168.43.173"
port = 8000

width = 1920
height = 1080
box_width = 10
start_speed = 2
title = "Lines: Battle Royale!"

number_of_players = 2
numbers = ["2", "3", "4", "5", "6"]
if len(sys.argv) == 2:
    if sys.argv[1] not in numbers:
        print("Incorrect number of players, setting the default: 2")
    else:
        print("Number of players:", sys.argv[1])
        number_of_players = int(sys.argv[1])

# SERVERS START RUNNING
servers = []
for i in range(0, number_of_players):
    time.sleep(0.1)
    servers.append(Server(host, port + i))

# APPLICATION STARTS
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.HWSURFACE, 32)
pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
surface = pygame.display.get_surface()
pygame.display.set_caption(title)
clock = pygame.time.Clock()

# CONNECTING TO PORTS
arrow_left = pygame.image.load("arrowleft.png")
arrow_right = pygame.image.load("arrowright.png")
arrow_down = pygame.image.load("arrowdown.png")
logobig = pygame.image.load("linesbig.png")
logobig_rect = logobig.get_rect()
font = pygame.font.Font("edosz.ttf", 30)
medfont = pygame.font.Font("edosz.ttf", 32)
bigfont = pygame.font.Font("edosz.ttf", 60)
C = Colors()
screen.fill(C.black)

connected_frames = 0
all_connected = False
while not all_connected:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                pygame.mouse.set_visible(False)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((width, height))
                pygame.mouse.set_visible(True)
    screen.fill(C.black)
    indent = int((width - logobig_rect.width) / 2)
    logobig_rect.x = indent
    logobig_rect.y = int(indent / 4)
    screen.blit(logobig, logobig_rect)

    text = font.render("Please connect to open ports:", True, C.white)
    temp_y = logobig_rect.y + indent
    temp_x = int((width - text.get_width()) / 2)
    screen.blit(text, (temp_x, temp_y))
    server_counter = 0
    temp_y += 50
    for s in servers:
        server_counter += 1
        temp_y += int(indent / 18)
        text = font.render("Player " + str(server_counter) + ":      " + s.host + ":" + str(s.port)
                           + ((" (Connected by " + s.client + ")") if s.connected else ""), True,
                           ((3, 125, 80) if s.connected else C.white))
        temp_x = int((width - text.get_width()) / 2)
        screen.blit(text, (temp_x, temp_y))
    if servers_connected(servers):
        temp_y += int(indent / 3)
        text = bigfont.render("All players connected! Starting soon:    " + str(5 - int(connected_frames / 60)) + "...",
                              True, (2, 100, 64))
        temp_x = int((width - text.get_width()) / 2)
        screen.blit(text, (temp_x, temp_y))
        connected_frames += 1
        print(connected_frames)
    else:
        connected_frames = 0
    if connected_frames == 300:
        all_connected = True
    pygame.display.flip()
    clock.tick(60)

# CHOSING COLORS
possible_colors = [(255, 255, 255, False), (224, 205, 255, False), (102, 255, 102, False), (102, 102, 255, False),
                   (255, 255, 0, False), (255, 0, 127, False), (0, 0, 153, False), (255, 0, 0, False),
                   (76, 153, 0, False)]

color_number = random.randint(0, len(possible_colors) - 1)
players_chose = []
for i in range(0, number_of_players):
    players_chose.append(False)

for s in servers:
    color_number = get_next_color(possible_colors, color_number)
    s.clear_queue()
    while not players_chose[s.port - port]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    pygame.mouse.set_visible(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((width, height))
                    pygame.mouse.set_visible(True)

        color = possible_colors[color_number]

        screen.fill(C.black)
        indent = int((width - logobig_rect.width) / 2)
        logobig_rect.x = indent
        logobig_rect.y = int(indent / 4)
        screen.blit(logobig, logobig_rect)

        text = font.render("Choose your color:", True, C.white)
        temp_y = int(logobig_rect.y + indent) - 100
        temp_x = int((width - text.get_width()) / 2)
        screen.blit(text, (temp_x, temp_y))

        text = bigfont.render("Player " + str(s.port + 1 - port) + ":", True, color)
        temp_y += int(indent / 10)
        temp_x = int((width - text.get_width()) / 2)
        screen.blit(text, (temp_x, temp_y))

        rect_side = 100
        temp_x = int((width - rect_side)/2)
        temp_y += int(indent / 4)
        pygame.draw.rect(screen, C.grey, pygame.Rect(temp_x - 5, temp_y - 5, rect_side + 10, rect_side + 10))
        pygame.draw.rect(screen, color, pygame.Rect(temp_x, temp_y, rect_side, rect_side))
        temp_x -= int(indent/4)
        temp_y += int((rect_side - arrow_left.get_rect().height) / 2)
        screen.blit(arrow_left, pygame.Rect(temp_x, temp_y, arrow_left.get_rect().width, arrow_left.get_rect().height))
        temp_x += int(indent/2) + rect_side - arrow_left.get_rect().width
        screen.blit(arrow_right, pygame.Rect(temp_x, temp_y, arrow_right.get_rect().width,
                                             arrow_right.get_rect().height))
        text = font.render("Confirm", True, C.white)
        temp_y += int(indent / 3)
        temp_x = int((width - text.get_width())/2)
        screen.blit(text, (temp_x, temp_y))
        temp_y += int(indent/16)
        temp_x = int((width - arrow_down.get_rect().width)/2)
        screen.blit(arrow_down, pygame.Rect(temp_x, temp_y, arrow_down.get_rect().width,
                                            arrow_down.get_rect().height))

        if not s.q.empty():
            command = s.q.get()
            if command == "LEFT":
                color_number = get_previous_color(possible_colors, color_number)
            elif command == "RIGHT":
                color_number = get_next_color(possible_colors, color_number)
            elif command == "DOWN":
                s.color = (possible_colors[color_number][0], possible_colors[color_number][1],
                           possible_colors[color_number][2])
                possible_colors[color_number] = (possible_colors[color_number][0], possible_colors[color_number][1],
                                                 possible_colors[color_number][2], True)
                players_chose[s.port - port] = True

        pygame.display.flip()
        clock.tick(60)


# MAIN GAMEPLAY
menu_width = int(0.2 * width)
width -= menu_width
text_fieldclosing = font.render("Field closing in:", True, C.white)
text_ranking = font.render("Ranking:", True, C.white)
logo = pygame.image.load("lines.png")
crown = pygame.image.load("crown.png")
logorect = logo.get_rect()
crownrect = crown.get_rect()
last_time = ""

S = StartingPoints()

game_ended = False
players = []
for i in range(0, number_of_players):
    players.append(Player(servers[i], S.random_point(), servers[i].color, random_direction(), start_speed))
S.reset()
C.reset()
screen.fill(C.black)
pygame.display.flip()

frame_counter = 1
fog_number = 1
waiting_for_round = True

draw_menu(players, frame_counter)
draw_outline(fog_number)
done = False

S.reset()
for i in range(0, number_of_players):
    players[i].reset()
    players[i].update()

for i in range(0, 180):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((width + menu_width, height), pygame.FULLSCREEN)
                pygame.mouse.set_visible(False)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((width + menu_width, height))
                pygame.mouse.set_visible(True)
    last_time = frame_counter
    frame_counter = i
    draw_menu(players, frame_counter)
    pygame.display.flip()
    clock.tick(60)

while not game_ended:
    waiting_for_round = False
    fog_closing = False
    fog_number = 1
    fog_current_percent = 0
    frame_counter = 1
    screen.fill(C.black)
    draw_menu(players, frame_counter)
    draw_outline(fog_number)
    done = False

    S.reset()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.set_mode((width + menu_width, height), pygame.FULLSCREEN)
                    pygame.mouse.set_visible(False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.set_mode((width + menu_width, height))
                    pygame.mouse.set_visible(True)

        if players_connected(players):
            if not fog_closing:
                frame_counter += 1
            if frame_counter % 30 == 0:
                for i in range(0, number_of_players):
                    players[i].toggle_show()
            for i in range(0, number_of_players):
                check_player = players[i].update()
                if not check_player:
                    players[i].stop()
            if players_stopped(players):
                moving_player = find_moving_player(players)
                if moving_player is not None:
                    moving_player.points += 100
                    screen.blit(crown, (moving_player.x - 11, moving_player.y - 35))
                draw_menu(players, frame_counter)
                pygame.display.flip()
                for i in range(0, 180):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F11:
                                pygame.display.set_mode((width + menu_width, height), pygame.FULLSCREEN)
                                pygame.mouse.set_visible(False)
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.display.set_mode((width + menu_width, height))
                                pygame.mouse.set_visible(True)
                    waiting_for_round = True
                    last_time = frame_counter
                    frame_counter = i
                    draw_menu(players, frame_counter)
                    pygame.display.flip()
                    clock.tick(60)
                done = True
            if not fog_closing:
                draw_outline(fog_number)
                if frame_counter is not 0 and frame_counter % 601 == 0:
                    fog_closing = True
                    frame_counter = 0
            else:
                draw_fog(fog_current_percent, fog_number)
                fog_current_percent += 0.5
                if fog_current_percent > 100:
                    fog_current_percent = 0
                    fog_closing = False
                    frame_counter = 1
                    fog_number += 1
        most_points = draw_menu(players, frame_counter)
        if most_points >= 1000:
            game_ended = True
        pygame.display.flip()
        clock.tick(60)

    for i in range(0, number_of_players):
        players[i].reset()
        players[i].change_starting_point(S.random_point(), random_direction())
        players[i].update()


# ON GAME ENDED
players.sort(key=get_points, reverse=True)
width = width + menu_width
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit(0)
    screen.fill(C.black)
    indent = int((width - logobig_rect.width) / 2)
    logobig_rect.x = indent
    logobig_rect.y = int(indent / 4)
    screen.blit(logobig, logobig_rect)

    text = bigfont.render("Winner - Player " + str(players[0].server.port + 1 - port) + ": "
                          + str(int(players[0].points)) + " points", True, players[0].color)
    temp_y = logobig_rect.y + indent
    temp_x = int((width - text.get_width()) / 2)
    screen.blit(text, (temp_x, temp_y))
    player_num = 1
    temp_y += int(indent/10)
    for r in range(1, number_of_players):
        _x = players[r]
        temp_y += int(indent/15)
        player_num += 1
        text_player_ranking = font.render(str(player_num) + ". Player " + str(_x.server.port - (port - 1)) + ": " +
                                          str(int(_x.points)) + " points", True, _x.color)
        temp_x = int((width - text_player_ranking.get_width()) / 2)
        screen.blit(text_player_ranking, (temp_x, temp_y))

    pygame.display.flip()
    clock.tick(60)
