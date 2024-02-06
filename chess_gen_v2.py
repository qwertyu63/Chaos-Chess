from random import randint
from math import ceil

class piece(object):
    def __init__(self):
        self.value = 0
        self.bind = 9
        self.sight = [[], []]
        self.moves = []
        self.name = ""
        self.code = ""
        self.letter = ""
        self.lock = []

    def royal_blood(self):
        self.moves = [nor_atoms[0], nor_atoms[1]]
        self.compile()
        self.name = "King"

    def add_move(self, move):
        accept = True
        if move.lock not in self.lock:
            self.moves.append(move)
            self.lock.append(move.lock)

    def compile(self):
        new_code = ""
        parts = []
        self.value = 0
        self.bind = 9
        self.moves.sort(key=lambda x: x.id)

        for i in self.moves:
            new_code += i.code
            parts.append(i.code)
            for j in i.sight[0]:
                if j not in self.sight[0]:
                    self.sight[0].append(j)
            for j in i.sight[1]:
                if j not in self.sight[1]:
                    self.sight[1].append(j)
            self.value += i.value
            if self.bind > i.bind:
                self.bind = i.bind
        self.value -= self.bind

        self.code = new_code
        self.name_gen()

    def name_gen(self):
        if self.code in prebuild.keys():
            self.name = prebuild[self.code]
        else:
            self.name = ""
            cleancode = self.code.replace("[", "").replace("]", "")
            name_len = 3
            if len(cleancode) <= name_len:
                name_len = len(cleancode)
            for i in cleancode[0:name_len]:
                self.name += i
                if i not in ["A", "E", "I", "O", "U"]:
                    self.name += ["A", "E", "I", "O", "U"][randint(0,4)]
                self.name = self.name.title()

    def describe(self, full=False):
        line = self.letter + ": " + self.name + " (" + self.code + ")"
        if full:
            line += " [" + str(self.value) + "]"
        return line

    def set_letter(self, default, list):
        self.letter = ""
        if len(self.code) == 1:
            self.letter = self.code
        elif self.name == "King":
            self.letter = "K"
        elif self.name == "Queen":
            self.letter = "Q"
        else:
            for i in self.name:
                if i.upper() not in list:
                    if i.upper() not in "WFDANRBKQP":
                        self.letter = i.upper()
            if self.letter == "":
                self.letter = default
        return self.letter

class move(object):
    def __init__(self, id, code, value, bind, sight, reach, lock, dir = ["f", "b", "s"]):
        self.id = id
        self.code = code
        self.value = value
        self.bind = bind
        self.sight = sight
        self.reach = reach
        self.lock = lock
        self.dir = dir

    def clone(self, offset):
        new_id = self.id + offset
        return move(new_id, self.code, self.value, self.bind, self.sight, self.reach, self.lock)

    def peace_war(self, peace="True"):
        if peace:
            self.sight = [[], []]
            self.value *= 0.6
            self.code += "m"
        else:
            self.bind = 9
            self.value *= 0.4
            self.code += "a"

    def bent_ride(self):
        step_roll = randint(0,6)
        if step_roll >= 5: step_roll -= 5
        first_step = nor_atoms[step_roll]
        if first_step.code not in self.lock:
            new_code = "t["+first_step.code+self.code+"]"
            self.value *= 1.8
            if first_step.code == "N": self.value *= 1.8
            self.sight = first_step.sight
            self.code = new_code
            self.lock = first_step.lock
        if first_step.bind < self.bind:
            self.bind = first_step.bind

    def __str__(self):
        return self.code

nor_atoms = [
    move(0, "W", 2, 0, [[0], []], 1, "W"),
    move(1, "F", 2, 1, [[1], []], 1, "F"),
    move(2, "D", 1, 2, [[], [0]], 1, "D"),
    move(3, "A", 1, 3, [[], [2]], 1, "A"),
    move(4, "N", 3, 0, [[2], [1]], 1, "N"),
    move(5, "R", 4, 0, [[0], []], 1, "W"),
    move(6, "B", 5, 1, [[1], []], 1, "F"),
]

long_atoms = [
    move(7, "C", 3, 1, [[3], []], 2, "C"),
    move(8, "Z", 2, 0, [[], [3]], 2, "Z"),
    move(9, "H", 1, 9, [[], []], 2, "H"),
]

rare_atoms = [
    move(10, "DD", 2, 2, [[], [0]], 2, "D"),
    move(11, "AA", 2, 3, [[], [2]], 2, "A"),
    move(12, "NN", 5, 0, [[2], [1]], 2, "N"),    
]

def gen_piece(big = False, even_strike = True):
    roll = [1, 2, 2, 2, 3, 3][randint(0, 5)]
    new_piece = piece()
    while roll >= 1:
        if big and randint(0,1):
            if randint(0,3) == 0 and even_strike:
                side = rare_atoms[randint(0, len(rare_atoms)-1)]
            else:
                side = long_atoms[randint(0, len(long_atoms)-1)]
        else:
            side = nor_atoms[randint(0,len(nor_atoms)-1)]
        count = 1
        if randint(1,3) == 1:
            first = not bool(len(new_piece.moves))
            side, count = gen_chaos(side, first)
        new_piece.add_move(side)
        roll -= count
    new_piece.compile()
    return new_piece

def gen_chaos(side, first = False):
    chaosroll = randint(1,3)
    new_side = side.clone(100*chaosroll)
    restrict = False
    count = 1
    if chaosroll == 1:
        new_side.peace_war()
        restrict = True
    elif chaosroll == 2:
        new_side.peace_war(False)
        restrict = True
    elif chaosroll == 3:
        new_side.bent_ride()
        count = 2
    if restrict and first:
        return side, count
    else:
        return new_side, count

def pawn_check(pieces, slots, row, reach = 0):
    for i, j in enumerate(slots):
        if j:
            sight = pieces[j].sight[reach]
            for x in sight:
                if i-x >= 0: row[i-x]=True
                if i+x < len(row): row[i+x]=True
    return row

def push_name(piece, box):
    if piece.code in prebuild.keys():
        if piece.value > box[1][1]:
            box[1] = [piece.name, piece.value]
    else:
        if piece.value > box[0][1]:
            box[0] = [piece.name, piece.value]

# This is a list of default piece names.
prebuild = {
    "W": "Wazir", 
    "F": "Ferz", 
    "D": "Dabbaba", 
    "A": "Alfil", 
    "N": "Knight", 
    "R": "Rook", 
    "B": "Bishop", 
    "C": "Camel", 
    "Z": "Zebra", 
    "WF": "Man", 
    "WD": "Woodman", 
    "WA": "Phoenix", 
    "WN": "Marquis", 
    "WB": "Archbishop", 
    "WC": "Sorcerer", 
    "WZ": "Ranger", 
    "FD": "Scout", 
    "FA": "Preacher", 
    "FN": "Priest", 
    "FR": "Tower", 
    "FC": "Wizard", 
    "FZ": "Druid", 
    "DA": "Spider", 
    "DN": "Archer", 
    "DR": "Acrobat", 
    "DB": "Paladin", 
    "AN": "Hunter", 
    "AR": "Soldier", 
    "AB": "Shaman", 
    "NR": "Chancellor", 
    "NB": "Cardinal", 
    "NC": "Wildebeest", 
    "NZ": "Moose", 
    "NH": "Warlord", 
    "RB": "Queen", 
    "RC": "Barbarian", 
    "RZ": "Wanderer", 
    "BC": "Caliph", 
    "BZ": "Witch", 
    "CZ": "Ram", 
    "WFN": "Centaur", 
    "DAN": "Squirrel", 
    "WDA": "Champion", 
    "NCZ": "Dragon", 
    "NN": "Nightrider", 
    "DD": "Warmachine", 
    "AA": "Elephant Rider", 
    "BNN": "Unicorn", 
    "RNN": "Pegasus",
    "t[FR]": "Gryphon", 
    "t[WB]": "Anaca", 
    "t[DR]": "Lancer", 
    "t[AB]": "Monk", 
    "t[WF]": "Mule", 
}

# This is the start of the board generation.
while True:
    name_box = [["", -9], ["King", 0]]

    ranks = randint(6,13)
    files = randint(6,13)

    # ranks, files = 8,8

    if ranks + files >= 18:
        big_board = True
    else:
        big_board = False

    if ranks > randint(9,12):
        large_camp = True
    else:
        large_camp = False

    piece_count = files
    if large_camp:
        piece_count += files

    # If a leaping rider could attack the opposing back rank, we need to not use them.
    even_strike = not (ranks % 2 == 1 or large_camp)

    # If there are too many pieces, we half the piece count by making the board symmetrical.
    sym = piece_count >= randint(7,12)

    if sym:
        piece_count -= files//2
        if large_camp:
            piece_count -= files//2
            if files % 2 == 1:
                piece_count += 1
        if files % 2 == 0:
            piece_count += 1

    # This is a debug print.
    # print(str(files)+" files, "+str(piece_count)+" pieces, sym " + str(sym))

    king = piece()
    king.royal_blood()

    pieces = {"K": king}
    slots = ["K"]
    royal_home = files // 2

    # This section generates all of the pieces.
    while len(slots) != piece_count:
        new_piece = gen_piece(big_board, even_strike)
        if (new_piece.value <= 9 and new_piece.value >= 1) or new_piece.code in prebuild.keys():
            if new_piece.code not in pieces.keys():
                pieces[new_piece.code] = new_piece
            slots.append(new_piece.code)
            push_name(new_piece, name_box)

    # This section builds the starting board setup.
    true_pieces = ["K"]

    home_row = [""] * files
    counter = 1
    if sym:
        i = 0
        while i != royal_home:
            home_row[i] = slots[counter]
            home_row[-(i+1)] = slots[counter]
            if slots[counter] not in true_pieces:
                true_pieces.append(slots[counter])
            i+=1
            counter+=1
        home_row[royal_home] = "K"
    else:
        for i in range(0, files):
            if i == royal_home:
                home_row[i] = "K"
            else: 
                home_row[i] = slots[counter]
                if slots[counter] not in true_pieces:
                    true_pieces.append(slots[counter])
                counter+=1

    if large_camp:
        extra_row = [""] * files
        if sym:
            i = 0
            while i != royal_home:
                extra_row[i] = slots[counter]
                extra_row[-(i+1)] = slots[counter]
                if slots[counter] not in true_pieces:
                    true_pieces.append(slots[counter])
                counter+=1
                i += 1
            if files % 2 == 1:
                extra_row[royal_home] = slots[counter]
                if slots[counter] not in true_pieces:
                    true_pieces.append(slots[counter])
        else:
            for i in range(0, files):
                extra_row[i] = slots[counter]
                if slots[counter] not in true_pieces:
                    true_pieces.append(slots[counter])
                counter+=1

    # This section checks if every pawn is guarded.
    pawns_row = [False] * files
    if large_camp:
        pawns_row = pawn_check(pieces, extra_row, pawns_row)
        pawns_row = pawn_check(pieces, home_row, pawns_row, 1)
    else:
        pawns_row = pawn_check(pieces, home_row, pawns_row)

    # If any pawn is unguarded, the board must be rejected.
    safe_board = True
    for i in pawns_row:
        safe_board = safe_board and i
    if safe_board:
        break

# -------------------------
# If we get to this point, a valid starting condition has been generated.
# -------------------------

if name_box[0][0] != "":
    key_piece = name_box[0][0]
else:
    key_piece = name_box[1][0]

print(key_piece + " Chess:\n")

default_list = ["X", "V", "H", "J", "Y"]
default = default_list.pop(0)
letters_used = []

for i in pieces.keys():
    new = pieces[i].set_letter(default, letters_used)
    letters_used.append(new)
    if new == default:
        if default_list != []:
            default = default_list.pop(0)
        else:
            default = "?"
    if new in default_list: default_list.remove(new)

# This section prints the starting board state, with grid coordinates.

letters = "abcdefghijklmnopqrstuvwxyz"
if ranks >= 10:
    print("   ", end="")
else:
    print("  ", end="")
for i in range(0, files):
    print(letters[i], end="")
print()

ranks_left = ranks
rank_count=ranks

def label_rank(count):
    if ranks >= 10 and count < 10:
        print(" "+str(rank_count)+" ", end="")
    else:
        print(str(rank_count)+" ", end="")
    return count-1

rank_count = label_rank(rank_count)
for i in home_row:
    if i == "":
        print("-", end = "")
    else:
        print(pieces[i].letter.lower(), end = "")
ranks_left -= 2
print()

if large_camp:
    rank_count = label_rank(rank_count)
    for i in extra_row:
        if i == "":
            print("-", end = "")
        else:
            print(pieces[i].letter.lower(), end = "")
    ranks_left -= 2
    print()

rank_count = label_rank(rank_count)
print("p" * files)
ranks_left -= 2

while ranks_left:
    rank_count = label_rank(rank_count)
    print("-" * files)
    ranks_left -= 1

rank_count = label_rank(rank_count)
print("P" * files)

if large_camp:
    rank_count = label_rank(rank_count)
    for i in extra_row:
        if i == "":
            print("-", end = "")
        else:
            print(pieces[i].letter, end = "")
    print()

rank_count = label_rank(rank_count)
for i in home_row:
    if i == "":
        print("-", end = "")
    else:
        print(pieces[i].letter, end = "")

print()
print()

print("Piece List:")
for i in true_pieces:
    print(pieces[i].describe())

