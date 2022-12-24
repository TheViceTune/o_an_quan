from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QPlainTextEdit
from PyQt5.uic import loadUi
import os.path
from database import *
import time

import itertools
# Game board

board = [[5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
         [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]]
score_player1 = [0, 0]
score_player2 = [0, 0]

# Application
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi("Game Layout.ui", self)
        self.game_over = False
        self.turn = 0
        self.board = board
        self.one_owe_two = 0
        self.two_owe_one = 0
        self.moves = []
        self.quan = 2
        self.p1_moves = []
        self.p2_moves = []
        self.AI = False
        self.playAI = False
        self.p1_wins = 0
        self.p2_wins = 0

        # Set value
        self.slot0.setText(str(self.board[0][0]))
        self.slot1.setText(str(self.board[1][0]))
        self.slot2.setText(str(self.board[2][0]))
        self.slot3.setText(str(self.board[3][0]))
        self.slot4.setText(str(self.board[4][0]))
        self.slot5.setText(str(self.board[5][0]) + ", " + str(self.board[5][1]))
        self.slot6.setText(str(self.board[6][0]))
        self.slot7.setText(str(self.board[7][0]))
        self.slot8.setText(str(self.board[8][0]))
        self.slot9.setText(str(self.board[9][0]))
        self.slot10.setText(str(self.board[10][0]))
        self.slot11.setText(str(self.board[11][0]) + ", " + str(self.board[11][1]))
        self.p1_score.setText(str(score_player1))
        self.p2_score.setText(str(score_player2))



        # Define widgets
        self.button0 = self.findChild(QPushButton, "button0")
        self.button1 = self.findChild(QPushButton, "button1")
        self.button2 = self.findChild(QPushButton, "button2")
        self.button3 = self.findChild(QPushButton, "button3")
        self.button4 = self.findChild(QPushButton, "button4")
        self.button5 = self.findChild(QPushButton, "button6")
        self.button6 = self.findChild(QPushButton, "button7")
        self.button7 = self.findChild(QPushButton, "button8")
        self.button8 = self.findChild(QPushButton, "button9")
        self.button9 = self.findChild(QPushButton, "button10")
        self.clockwise = self.findChild(QPushButton, "clockwise")
        self.c_clockwise = self.findChild(QPushButton, "c_clockwise")
        self.start_game = self.findChild(QPushButton, "start_game")
        self.play_with_AI = self.findChild(QPushButton, "play_with_AI")
        self.AI_button = self.findChild(QPushButton, "AI_button")
        self.go_first = self.findChild(QPushButton, "go_first")
        self.go_second = self.findChild(QPushButton, "go_second")
        self.log_box = self.findChild(QPlainTextEdit, "log_box")
        self.turn_label = self.findChild(QLabel, "turn_label")
        self.gameover = self.findChild(QLabel, "gameover")

        # Hide everything
        self.button0.hide()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button5.hide()
        self.button6.hide()
        self.button7.hide()
        self.button8.hide()
        self.button9.hide()
        self.clockwise.hide()
        self.c_clockwise.hide()
        self.go_first.hide()
        self.go_second.hide()
        self.gameover.hide()
        self.turn_label.hide()

        # Click the button
        self.button0.clicked.connect(lambda: self.slot_picker(self.button0))
        self.button1.clicked.connect(lambda: self.slot_picker(self.button1))
        self.button2.clicked.connect(lambda: self.slot_picker(self.button2))
        self.button3.clicked.connect(lambda: self.slot_picker(self.button3))
        self.button4.clicked.connect(lambda: self.slot_picker(self.button4))
        self.button5.clicked.connect(lambda: self.slot_picker(self.button5))
        self.button6.clicked.connect(lambda: self.slot_picker(self.button6))
        self.button7.clicked.connect(lambda: self.slot_picker(self.button7))
        self.button8.clicked.connect(lambda: self.slot_picker(self.button8))
        self.button9.clicked.connect(lambda: self.slot_picker(self.button9))
        self.clockwise.clicked.connect(lambda: self.direction_picker(self.clockwise))
        self.c_clockwise.clicked.connect(lambda: self.direction_picker(self.c_clockwise))
        self.go_first.clicked.connect(self.first_player)
        self.go_second.clicked.connect(self.second_player)
        self.start_game.clicked.connect(self.gamestart)
        self.AI_button.clicked.connect(self.start_AI)
        self.play_with_AI.clicked.connect(self.play_AI)

        # Dicts
        self.slot = {self.button0: 0, self.button1: 1, self.button2: 2,
                     self.button3: 3, self.button4: 4, self.button5: 6,
                     self.button6: 7, self.button7: 8, self.button8: 9,
                     self.button9: 10}
        self.slotbutton = {self.button0: 1, self.button1: 2, self.button2: 3,
                           self.button3: 4, self.button4: 5, self.button5: 1,
                           self.button6: 2, self.button7: 3, self.button8: 4,
                           self.button9: 5}
        self.buttonslot = {0: self.button0, 1: self.button1, 2: self.button2, 3: self.button3,
                           4: self.button4, 6: self.button5, 7: self.button6, 8: self.button7,
                           9: self.button8, 10: self.button9}

        # Update func
    def update_slot(self):
        self.slot0.setText(str(self.board[0][0]))
        self.slot1.setText(str(self.board[1][0]))
        self.slot2.setText(str(self.board[2][0]))
        self.slot3.setText(str(self.board[3][0]))
        self.slot4.setText(str(self.board[4][0]))
        self.slot5.setText(str(self.board[5][0]) + ", " + str(self.board[5][1]))
        self.slot6.setText(str(self.board[6][0]))
        self.slot7.setText(str(self.board[7][0]))
        self.slot8.setText(str(self.board[8][0]))
        self.slot9.setText(str(self.board[9][0]))
        self.slot10.setText(str(self.board[10][0]))
        self.slot11.setText(str(self.board[11][0]) + ", " + str(self.board[11][1]))
        self.p1_score.setText(str(score_player1))
        self.p2_score.setText(str(score_player2))
        # Clicker
    def slot_picker(self, b):
        self.curslot = self.slot[b]
        self.empty(b)
        self.selection = self.slotbutton[b]
        if self.turn == 0:
            self.hide_p1()
        else:
            self.hide_p2()
        self.show_direction()
        print(self.selection)

    def direction_picker(self, a):
        self.state_dir = self.generate_database_location()
        self.moves = []
        self.direction_lib = {self.clockwise: "cl", self.c_clockwise: "c_cl"}
        self.direction = self.direction_lib[a]
        self.hide_direction()
        self.game_move()
        if self.playAI:
            if self.player_AI == "p1":
                self.hide_p2()
                self.make_a_turn()
            if self.player_AI == "p2":
                self.hide_p1()
                self.make_a_turn()

    def start_AI(self):
        self.AI = True
        self.playAI = False
        i = 0
        while i <= 1000:
            self.restart()
            self.cur_turn = 0
            while not self.game_over:
                self.make_a_turn()
                self.cur_turn += 1
                if self.cur_turn == 50:
                    self.end_game(self.p1_moves, self.p2_moves, False)
                    break
            i += 1
            print(i)
        print(self.p1_wins)
        print(self.p2_wins)

    def play_AI(self):
        self.AI = False
        self.playAI = True
        self.restart()
        self.go_first.show()
        self.go_second.show()
        self.play_with_AI.setText("Restart AI game")
        self.start_game.setText("Start Game")
        self.log_box.setPlainText("")
        self.update_slot()

    def first_player(self):
        self.show_p1()
        self.turn_label.setText("Player 1's turn")
        self.player_AI = "p1"
        self.go_first.hide()
        self.go_second.hide()

    def second_player(self):
        self.go_first.hide()
        self.go_second.hide()
        self.player_AI = "p2"
        self.make_a_turn()

    def restart(self):
        self.hide_all()
        self.turn = 0
        global board
        global score_player1
        global score_player2
        score_player1 = [0, 0]
        score_player2 = [0, 0]
        self.one_owe_two = 0
        self.two_owe_one = 0
        self.moves = []
        self.board = [[5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
         [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]]
        self.p1_moves = []
        self.p2_moves = []
        self.game_over = False
        self.state_dir = self.generate_database_location()
        self.turn_label.show()
        self.update_slot()

    def gamestart(self):
        self.AI = False
        self.playAI = False
        self.hide_all()
        self.turn = 0
        self.play_with_AI.setText("Play with AI")
        self.turn_label.setText("Player 1's turn")
        self.moves = []
        self.turn_label.show()
        self.show_p1()
        global board
        global score_player1
        global score_player2
        score_player1 = [0, 0]
        score_player2 = [0, 0]
        self.one_owe_two = 0
        self.two_owe_one = 0
        self.board = [[5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1],
         [5, 0], [5, 0], [5, 0], [5, 0], [5, 0], [0, 1]]
        self.p1_moves = []
        self.p2_moves = []
        self.start_game.setText("Restart")
        self.game_over = False
        self.state_dir = self.generate_database_location()
        self.log_box.setPlainText("")
        self.update_slot()

    def log_moves(self, selection, direction):
        move_string = ""
        slot_dict = {1: "Slot 1", 2: "Slot 2", 3: "Slot 3", 4: "Slot 4", 5: "Slot 5"}
        direct_dict = {"cl": "clockwise", "c_cl": "counter clockwise"}
        if not self.playAI:
            if self.turn == 0:
                move_string = "P1: " + str(slot_dict[selection]) + " " + str(direct_dict[direction])
            elif self.turn != 0:
                move_string = "P2: " + str(slot_dict[selection]) + " " + str(direct_dict[direction])
        if self.playAI:
            if self.player_AI == "p1":
                if self.turn == 0:
                    move_string = "Player: " + str(slot_dict[selection]) + " " + str(direct_dict[direction])
                elif self.turn != 0:
                    move_string = "Bot: " + str(slot_dict[selection]) + " " + str(direct_dict[direction])
            if self.player_AI == "p2":
                if self.turn == 0:
                    move_string = "Bot: " + str(slot_dict[selection]) + " " + str(direct_dict[direction])
                elif self.turn != 0:
                    move_string = "Player: " + str(slot_dict[selection]) + " " + str(direct_dict[direction])
        self.log_box.appendPlainText(move_string + "\n")

    # Show and hide
    def show_p1(self):
        self.button0.show()
        self.button1.show()
        self.button2.show()
        self.button3.show()
        self.button4.show()

    def show_p2(self):
        self.button5.show()
        self.button6.show()
        self.button7.show()
        self.button8.show()
        self.button9.show()

    def hide_p1(self):
        self.button0.hide()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()

    def hide_p2(self):
        self.button5.hide()
        self.button6.hide()
        self.button7.hide()
        self.button8.hide()
        self.button9.hide()

    def show_direction(self):
        self.clockwise.show()
        self.c_clockwise.show()

    def hide_direction(self):
        self.clockwise.hide()
        self.c_clockwise.hide()

    def hide_all(self):
        self.button0.hide()
        self.button1.hide()
        self.button2.hide()
        self.button3.hide()
        self.button4.hide()
        self.button5.hide()
        self.button6.hide()
        self.button7.hide()
        self.button8.hide()
        self.button9.hide()
        self.clockwise.hide()
        self.c_clockwise.hide()
        self.gameover.hide()
        self.go_first.hide()
        self.go_second.hide()

    # Game functions
    def add_score(self, point, player):
        while point[0] > 0:
            player[0] += 1
            point[0] -= 1
        while point[1] == 1:
            player[1] += 1
            point[1] -= 1

    def reset_counter(self, cnt):
        x = 11
        while x > 0:
            next(cnt)
            x -= 1

    def scatter(self, field, stone, count, score_player):
        while stone > 0:
            while stone > 0:
                field[next(count)][0] += 1
                stone -= 1
            if next(count) not in (5, 11):
                self.reset_counter(count)
                stone = field[next(count)][0]
                self.reset_counter(count)
                field[next(count)][0] = 0
            else:
                self.reset_counter(count)
        self.reset_counter(count)
        while field[next(count)] == [0, 0] and field[next(count)] != [0, 0]:
            self.reset_counter(count)
            next_stones = field[next(count)]
            self.add_score(next_stones, score_player)
            self.reset_counter(count)
            field[next(count)] = [0, 0]
        # print(field)

    def check_win(self):
        if self.board[5][1] == 0 and self.board[11][1] == 0:
            self.total_score1 = score_player1[0] + score_player1[1] * 10 - self.one_owe_two + self.two_owe_one
            self.total_score2 = score_player2[0] + score_player2[1] * 10 + self.one_owe_two - self.two_owe_one
            # print("Game Over!")
            if self.total_score1 > self.total_score2:
                if not self.playAI:
                    print("Player 1 wins")
                    self.gameover.setText("Game over, Player 1 wins!")
                if self.playAI:
                    if self.player_AI == "p1":
                        print("Player wins")
                        self.gameover.setText("Game over, Player wins!")
                    elif self.player_AI == "p2":
                        print("Bot wins")
                        self.gameover.setText("Game over, Bot wins")
                if self.AI:
                    self.p1_wins += 1
                    winner = self.p1_moves
                    loser = self.p2_moves
                    self.end_game(winner, loser, True)
            elif self.total_score1 < self.total_score2:
                if not self.playAI:
                    print("Player 2 wins")
                    self.gameover.setText("Game over, Player 2 wins!")
                if self.playAI:
                    if self.player_AI == "p2":
                        print("Player wins")
                        self.gameover.setText("Game over, Player wins!")
                    elif self.player_AI == "p1":
                        print("Bot wins")
                        self.gameover.setText("Game over, Bot wins")
                if self.AI:
                    self.p2_wins += 1
                    winner = self.p2_moves
                    loser = self.p1_moves
                    self.end_game(winner, loser, True)
            else:
                print("Draw!")
                self.gameover.setText("Game over, Draw!")
                if self.AI:
                    winner = self.p2_moves
                    loser = self.p1_moves
                    self.end_game(winner, loser, False)
            self.gameover.show()
            self.game_over = True
            if not self.AI:
                self.hide_all()
                self.gameover.show()

    def empty(self, b):
        self.slot = {self.button0: 0, self.button1: 1, self.button2: 2,
                    self.button3: 3, self.button4: 4, self.button5: 6,
                    self.button6: 7, self.button7: 8, self.button8: 9,
                    self.button9: 10}
        x = 0
        y = 0
        for n in (0, 1, 2, 3, 4):
            if self.board[n][0] == 0:
                x += 1
        for m in (6, 7, 8, 9, 10):
            if self.board[m][0] == 0:
                y += 1
        if x == 5:
            if self.turn == 0:
                if score_player1[0] >= 5:
                    score_player1[0] -= 5
                    self.board[self.slot[b]][0] = 5
                elif score_player1[0] < 5 <= score_player2[0]:
                    score_player2[0] -= 5
                    self.board[self.slot[b]][0] = 5
                    self.one_owe_two += 5
                else:
                    pass
        elif y == 5:
            if self.turn != 0:
                if score_player2[0] >= 5:
                    score_player2[0] -= 5
                    self.board[self.slot[b]][0] = 5
                elif score_player2[0] < 5 <= score_player1[0]:
                    score_player1[0] -= 5
                    self.board[self.slot[b]][0] = 5
                    self.one_owe_two += 5
                else:
                    pass
        self.update_slot()

    def empty2(self):
        x = 0
        y = 0
        if self.turn == 0:
            for n in (0, 1, 2, 3, 4):
                if self.board[n][0] == 0:
                    x += 1
            if x == 5:
                if score_player1[0] >= 5:
                    score_player1[0] -= 5
                    self.board[int(self.empty_slot)][0] = 5
                elif score_player1[0] < 5 <= score_player2[0]:
                    score_player2[0] -= 5
                    self.board[int(self.empty_slot)][0] = 5
                    self.one_owe_two += 5
                else:
                    pass
        if self.turn != 0:
            for m in (6, 7, 8, 9, 10):
                if self.board[m][0] == 0:
                    y += 1
            if y == 5:
                if score_player2[0] >= 5:
                    score_player2[0] -= 5
                    self.board[int(self.empty_slot)][0] = 5
                elif score_player2[0] < 5 <= score_player1[0]:
                    score_player1[0] -= 5
                    self.board[int(self.empty_slot)][0] = 5
                    self.two_owe_one += 5
                else:
                    pass

    def check_empty(self):
        x = 0
        y = 0
        for n in (0, 1, 2, 3, 4):
            if self.board[n][0] == 0:
                x += 1
        for m in (6, 7, 8, 9, 10):
            if self.board[m][0] == 0:
                y += 1
        if x == 5:
            if self.turn == 0:
                self.show_p1()
            else:
                pass
        elif y == 5:
            if self.turn != 0:
                self.show_p2()
            else:
                pass
        self.update_slot()

    def check_for_zero(self):
        for x in (0, 1, 2, 3, 4, 6, 7, 8, 9, 10):
            if self.board[x][0] == 0:
                self.buttonslot[x].hide()

    def check_valid_moves(self):
        self.moves = []
        if self.turn == 0:
            for i in (0, 1, 2, 3, 4):
                if self.board[i][0] != 0:
                    self.moves.append(i)
            if not self.moves:
                self.moves = [0, 1, 2, 3, 4]
        if self.turn != 0:
            for i in (6, 7, 8, 9, 10):
                if self.board[i][0] != 0:
                    self.moves.append(i)
            if not self.moves:
                self.moves = [6, 7, 8, 9, 10]
        return self.moves

    def write_valid_moves(self):
        jsonFileString = self.state_dir
        data = {}
        for m in self.check_valid_moves():
            data[m] = {}
            for i in ("cl", "c_cl"):
                data[m][i] = {}
                data[m][i]["w"] = 1
                data[m][i]["l"] = 1
        writeData(jsonFileString, data)

    def json_file_exists(self):
        dblocationstring = self.state_dir
        if not os.path.exists(dblocationstring):
            return False
        else:
            return True

    def make_a_turn(self):
        self.state_dir = self.generate_database_location()
        if not self.json_file_exists():
            self.check_valid_moves()
            self.write_valid_moves()
        self.move_piece()

    def get_best_selected(self):
        jsonFileString = "C:\\Users\Admin\PycharmProjects\oanquan\db\\2\\10\\0,0,0,1,1,4,2,0,0,0,0,2,\Player 1\data.json"
        data = loadData(jsonFileString)
        slot = ""
        chance = 0
        direction = ""
        for s in data:
            for d in data[s]:
                move_chance = data[s][d]["w"]/(data[s][d]["w"] + data[s][d]["l"])
                if move_chance > chance:
                    chance = move_chance
                    slot = s
                    direction = d
        result = [slot, direction]
        return result

    def get_quan(self):
        if self.board[5][1] == 1:
            if self.board[11][1] == 1:
                self.quan = 2
            elif self.board[11][1] == 0:
                self.quan = 11
        elif self.board[5][1] == 0:
            if self.board[11][1] == 1:
                self.quan = 12
            elif self.board[11][1] == 0:
                self.quan = 0
        return self.quan

    def get_pebbles(self):
        self.pebbles = 0
        for x in range(0, 12):
            self.pebbles += self.board[x][0]
        return self.pebbles

    def get_arrangement(self):
        self.arrangement = ""
        for x in range(0, 12):
            self.arrangement += str(self.board[x][0]) + ","
        return self.arrangement

    def get_player(self):
        self.curplayer = ""
        if self.turn == 0:
            self.curplayer = "Player 1"
        elif self.turn != 0:
            self.curplayer = "Player 2"
        return self.curplayer

    def generate_database_location(self):
        dbLocationString = os.path.abspath(os.curdir) + "/db/"
        dbLocationString += str(self.get_quan()) + "/"
        if not os.path.exists(dbLocationString):
            os.makedirs(dbLocationString)
        dbLocationString += str(self.get_pebbles()) + "/"
        if not os.path.exists(dbLocationString):
            os.makedirs(dbLocationString)
        dbLocationString += str(self.get_arrangement()) + "/"
        if not os.path.exists(dbLocationString):
            os.makedirs(dbLocationString)
        dbLocationString += str(self.get_player()) + "/"
        if not os.path.exists(dbLocationString):
            os.makedirs(dbLocationString)
        return dbLocationString + "data.json"

    def get_best_move(self):
        jsonFileString = self.state_dir
        data = loadData(jsonFileString)
        slot = ""
        chance = 0
        direction = ""
        for s in data:
            for d in data[s]:
                move_chance = data[s][d]["w"]/(data[s][d]["w"] + data[s][d]["l"])
                if move_chance > chance:
                    chance = move_chance
                    slot = s
                    direction = d
        result = [slot, direction]
        return result

    def move_piece(self):
        move = self.get_best_move()
        self.slot_to_num = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5,
                            6: 1, 7: 2, 8: 3, 9: 4, 10: 5}
        self.curslot = str(move[0])
        self.selection = str(self.slot_to_num[int(move[0])])
        self.empty_slot = int(move[0])
        self.direction = str(move[1])
        self.game_move()

    def record_moves(self):
        if self.turn == 0:
            self.p1_moves.append([self.state_dir, self.curslot, self.direction])
        elif self.turn != 0:
            self.p2_moves.append([self.state_dir, self.curslot, self.direction])
        # print(self.p1_moves)
        # print(self.p2_moves)

    def increment_move_chance(self, game_state, slot, direction, win):
        jsonFileString = game_state
        data = loadData(jsonFileString)
        if win:
            data[slot][direction]["w"] += 1
        else:
            data[slot][direction]["l"] += 1
        if data[slot][direction]["w"] % 2 == 0 and data[slot][direction]["l"] % 2 == 0:
            data[slot][direction]["w"] /= 2
            data[slot][direction]["l"] /= 2
        if data[slot][direction]["w"] % 3 == 0 and data[slot][direction]["l"] % 3 == 0:
            data[slot][direction]["w"] /= 3
            data[slot][direction]["l"] /= 3
        writeData(jsonFileString, data)

    def end_game(self, winner, loser, not_draw):
        if not_draw:
            for i in range(len(winner)):
                game_state = winner[i][0]
                slot = winner[i][1]
                direction = winner[i][2]
                self.increment_move_chance(game_state, slot, direction, True)
            for i in range(len(loser)):
                game_state = loser[i][0]
                slot = loser[i][1]
                direction = loser[i][2]
                self.increment_move_chance(game_state, slot, direction, False)
        elif not not_draw:
            for i in range(len(winner)):
                game_state = winner[i][0]
                slot = winner[i][1]
                direction = winner[i][2]
                self.increment_move_chance(game_state, slot, direction, False)
            for i in range(len(loser)):
                game_state = loser[i][0]
                slot = loser[i][1]
                direction = loser[i][2]
                self.increment_move_chance(game_state, slot, direction, False)

    def game_move(self):
        self.empty2()
        if self.turn == 0:
            if self.direction.upper() == "C_CL":
                lst = itertools.cycle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
                counter = itertools.islice(lst, int(self.selection), None)
                stones = self.board[int(self.selection) - 1][0]
                self.board[int(self.selection) - 1][0] = 0
                self.scatter(self.board, stones, counter, score_player1)
            elif self.direction.upper() == "CL":
                lst = itertools.cycle([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
                counter = itertools.islice(lst, 11 - int(self.selection), None)
                next(counter)
                next(counter)
                stones = self.board[int(self.selection) - 1][0]
                self.board[int(self.selection) - 1][0] = 0
                self.scatter(self.board, stones, counter, score_player1)
            if not self.AI:
                self.show_p2()
                self.turn_label.setText("Player 2's turn")
        else:
            if self.direction.upper() == "C_CL":
                lst = itertools.cycle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
                counter = itertools.islice(lst, int(self.selection) + 6, None)
                stones = self.board[int(self.selection) + 5][0]
                self.board[int(self.selection) + 5][0] = 0
                self.scatter(self.board, stones, counter, score_player2)
            elif self.direction.upper() == "CL":
                lst = itertools.cycle([11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
                counter = itertools.islice(lst, 5 - int(self.selection), None)
                next(counter)
                next(counter)
                stones = self.board[int(self.selection) + 5][0]
                self.board[int(self.selection) + 5][0] = 0
                self.scatter(self.board, stones, counter, score_player2)
            if not self.AI:
                self.show_p1()
                self.turn_label.setText("Player 1's turn")
        if not self.AI:
            self.log_moves(int(self.selection), self.direction)
        self.record_moves()
        self.check_win()
        self.turn += 1
        self.turn = self.turn % 2
        if not self.AI:
            self.check_for_zero()
            self.check_empty()
            self.update_slot()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()

