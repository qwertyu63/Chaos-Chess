# This program randomly generates chess variants.
# It randomly selects the board size and then generates an assortment of pieces to fill it.
# It considers the board size when creating pieces to create.
# It runs a check to make sure all pawns are protected in the opening layout, starting over if it isn't.
# It then displays the new variant in an easily readable format.

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
        '''This method turns this piece into a King.'''
        self.moves = [nor_atoms[0], nor_atoms[1]]
        self.compile()
        self.name = "King"

    def add_move(self, move):
        '''This method adds the provided move to this piece, provided it isn't redundant.'''
        accept = True
        if move.lock not in self.lock:
            self.moves.append(move)
            self.lock.append(move.lock)

    def compile(self):
        '''This method runs through the piece's moves, recording each to create the pieces code and name.'''
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
        '''This method determines the name of the piece.'''
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
        '''This method sets and stores the letter for this piece.'''
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
    def __init__(self, id, code, value, bind, sight, reach, lock, dir):
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
        return move(new_id, self.code, self.value, self.bind, self.sight, self.reach, self.lock, self.dir)

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

    def breaker(self, hard_lock = ""):
        if hard_lock:
            dir_lock = hard_lock
        else:
            dir_lock = self.dir[randint(0,len(self.dir)-1)]
        self.value /= 2
        if ("s" in self.dir) and (dir_lock != "s"):
            if randint(0, 1):
                self.value /= 2
            else:
                dir_lock = "fb"
        if dir_lock not in ["f", "fb"]:
            self.sight = [[], []]
        self.code += dir_lock
        return dir_lock

    def __str__(self):
        return self.code

# (id, code, value, bind, sight, reach, lock, dir)
# This section lists the basic move atoms.
nor_atoms = [
    move(0, "W", 2, 0, [[0], []], 1, "W", ["f", "b", "s"]),
    move(1, "F", 2, 1, [[1], []], 1, "F", ["f", "b"]),
    move(2, "D", 1, 2, [[], [0]], 1, "D", ["f", "b", "s"]),
    move(3, "A", 1, 3, [[], [2]], 1, "A", ["f", "b"]),
    move(4, "N", 3, 0, [[2], [1]], 1, "N", ["f", "b"]),
    move(5, "R", 4, 0, [[0], []], 1, "W", ["f", "b", "s"]),
    move(6, "B", 5, 1, [[1], []], 1, "F", ["f", "b"]),
]

long_atoms = [
    move(7, "C", 3, 1, [[3], []], 2, "C", ["f", "b"]),
    move(8, "Z", 2, 0, [[], [3]], 2, "Z", ["f", "b"]),
    move(9, "H", 1, 9, [[], []], 2, "H", ["f", "b", "s"]),
]

rare_atoms = [
    move(10, "DD", 2, 2, [[], [0]], 2, "D", ["f", "b", "s"]),
    move(11, "AA", 2, 3, [[], [2]], 2, "A", ["f", "b"]),
    move(12, "NN", 5, 0, [[2], [1]], 2, "N", ["f", "b"]),    
]

def gen_piece(big = False, even_strike = True):
    '''This function generates a new piece.'''
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
    '''This function takes a normal move and makes it chaotic in some fashion.'''
    chaosroll = randint(1,4)
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
    elif chaosroll == 4:
        dir_lock = new_side.breaker()
        if dir_lock in ["f", "b"] and first:
            count = 0
    if restrict and first:
        return side, count
    else:
        return new_side, count

def pawn_check(pieces, slots, row, reach = 0):
    '''This function takes a row of pieces and calculates which pawns it protects.'''
    for i, j in enumerate(slots):
        if j:
            sight = pieces[j].sight[reach]
            for x in sight:
                if i-x >= 0: row[i-x]=True
                if i+x < len(row): row[i+x]=True
    return row

def push_name(piece, box):
    '''This function updates the tracking of piece names and power used to determine the piece that names the game.'''
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

    ranks = randint(5,13)
    files = randint(5,13)

    # If the board is wide enough, we will enable the use of long leapers and leaping riders.
    if ranks + files >= 18:
        big_board = True
    else:
        big_board = False

    # If the board is long enough, we might add a second row of pieces.
    if ranks > randint(9,14):
        large_camp = True
    else:
        large_camp = False


    # If a leaping rider could attack the opposing back rank, we need to not use them.
    even_strike = not ranks % 2 == 1

    # This calulates how many pieces will be needed.
    piece_count = files
    if large_camp:
        piece_count += files

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

    # This creates the starting piece list, adding the all-important King to the set.
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

# This assigns a letter to each piece, used to indicate it on the board.
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

# This stores the number of empty ranks, for use later.
empty_ranks = ranks_left

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

# This section generates the list of moves.
print("Piece List:")
for i in true_pieces:
    print(pieces[i].describe())
print()

print("""Rules:
All normal chess rules apply, except as noted below.""")

if empty_ranks >= 6:
    print("Pawns may move three spaces on their first move. En passant can occur on either skipped space.")
if empty_ranks <= 3:
    print("Pawns do not have their double step move option.")

castle = "two"
if files >= 10: castle = "three"

if files >= randint(7, 9):
    print("The King can castle with the pieces in the corners of its starting rank. All normal castling rules apply; the king moves "+castle+" spaces towards the piece.")
else:
    print("There is no castling.")